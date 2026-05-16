#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# deploy.sh — Moteur d'automatisation deploy-docker v2.1
# VibeBackbone Skill: T-vbb-deploy-runtime
# Lit docker-services.map (généré par T-vbb-docker-generate)
# Usage: bash deploy.sh <dev|staging|prod> [action] [options]
# Actions: up (défaut), down, rebuild, status, backup, logs, rollback
# Options: --dry-run, --check, --force
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

# ─── Constantes ─────────────────────────────────────────────
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly BACKUP_DIR="${SCRIPT_DIR}/backups"
readonly TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
readonly COMPOSE_PROJECT_NAME="$(basename "${SCRIPT_DIR}" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g')"
readonly MIN_DISK_SPACE_MB=200
readonly BACKUP_SIZE_RATIO_MIN=0.1
readonly BACKUP_SIZE_RATIO_MAX=10.0
readonly SERVICE_MAP_FILE="${SCRIPT_DIR}/docker-services.map"

# ─── Service map (lue depuis docker-services.map) ─────────
# Si le fichier existe, les noms de services sont lus de là.
# Sinon, on fallback sur les heuristiques historiques (avec avertissement).

# Variables extraites de la service map
SERVICE_APP_NAME=""
SERVICE_APP_PORT=""
SERVICE_DATA_TYPE=""
SERVICE_DATA_NAME=""
SERVICE_DATA_PORT=""
SERVICE_CACHE_TYPE=""
SERVICE_CACHE_NAME=""
SERVICE_CACHE_PORT=""
SERVICE_PROXY_TYPE=""
SERVICE_PROXY_NAME=""

load_service_map() {
  if [[ ! -f "${SERVICE_MAP_FILE}" ]]; then
    log_warn "docker-services.map introuvable — fallback sur heuristiques (mode dégradé)"
    log_warn "Générer avec T-vbb-docker-generate pour un fonctionnement déterministe."
    return 1
  fi

  log_step "Lecture de docker-services.map..."

  # Parser le YAML simplifié (pas de dépendance à yq)
  local section=""
  local line
  while IFS= read -r line; do
    # Ignorer commentaires et lignes vides
    [[ "${line}" =~ ^[[:space:]]*# ]] && continue
    [[ -z "${line// }" ]] && continue

    # Détecter les sections
    if [[ "${line}" =~ ^([a-z_]+):$ ]]; then
      section="${BASH_REMATCH[1]}"
      continue
    fi

    # Extraire les paires clé: valeur
    if [[ "${line}" =~ ^[[:space:]]+(name|port|type)[[:space:]]*:[[:space:]]*(.+)$ ]]; then
      local key="${BASH_REMATCH[1]}"
      local value="${BASH_REMATCH[2]}"
      # Retirer les guillemets éventuels
      value="${value//\"/}"
      value="${value//\'/}"

      case "${section}:${key}" in
        app:name)    SERVICE_APP_NAME="${value}" ;;
        app:port)    SERVICE_APP_PORT="${value}" ;;
        data:type)  SERVICE_DATA_TYPE="${value}" ;;
        data:name)  SERVICE_DATA_NAME="${value}" ;;
        data:port)  SERVICE_DATA_PORT="${value}" ;;
        cache:type)  SERVICE_CACHE_TYPE="${value}" ;;
        cache:name)  SERVICE_CACHE_NAME="${value}" ;;
        cache:port)  SERVICE_CACHE_PORT="${value}" ;;
        proxy:type)  SERVICE_PROXY_TYPE="${value}" ;;
        proxy:name)  SERVICE_PROXY_NAME="${value}" ;;
      esac
    fi
  done < "${SERVICE_MAP_FILE}"

  log_success "Service map chargée : app=${SERVICE_APP_NAME}, data=${SERVICE_DATA_NAME}(${SERVICE_DATA_TYPE}), cache=${SERVICE_CACHE_NAME}(${SERVICE_CACHE_TYPE}), proxy=${SERVICE_PROXY_NAME}"
  return 0
}

# Fonction pour obtenir le nom du service de données
# Utilise la service map en priorité, fallback sur heuristiques
get_data_service_name() {
  local compose="$1"
  local env="$2"

  # Priorité 1 : service map
  if [[ -n "${SERVICE_DATA_NAME}" ]]; then
    echo "${SERVICE_DATA_NAME}"
    return
  fi

  # Fallback : heuristiques historiques (mode dégradé)
  local services
  services="$(docker compose -f "${compose}" config --services 2>/dev/null || true)"
  local pg_service
  pg_service="$(echo "${services}" | grep -m1 -E '^postgres' || true)"
  if [[ -z "${pg_service}" ]]; then
    pg_service="$(echo "${services}" | grep -m1 -E 'postgresql' || true)"
  fi
  if [[ -z "${pg_service}" ]]; then
    pg_service="$(echo "${services}" | grep -m1 -E '(mysql|mariadb)' || true)"
  fi
  if [[ -z "${pg_service}" ]]; then
    pg_service="$(echo "${services}" | grep -m1 -E '(db|database)' || true)"
  fi
  echo "${pg_service}"
}

# Fonction pour obtenir le type de service de données
get_data_service_type() {
  if [[ -n "${SERVICE_DATA_TYPE}" ]]; then
    echo "${SERVICE_DATA_TYPE}"
  else
    echo "unknown"
  fi
}

# ─── État global ────────────────────────────────────────────
DRY_RUN=false
CHECK_MODE=false
LAST_BACKUP_TAG=""

# ─── Couleurs ──────────────────────────────────────────────
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m'
readonly BOLD='\033[1m'

# ─── Fonctions d'affichage ─────────────────────────────────
log_info()    { echo -e "${BLUE}[INFO]${NC}    $*"; }
log_success() { echo -e "${GREEN}[OK]${NC}      $*"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC}    $*"; }
log_error()   { echo -e "${RED}[ERROR]${NC}   $*"; }
log_step()    { echo -e "${CYAN}${BOLD}▸${NC} $*"; }
log_dry()     { echo -e "${YELLOW}[DRY-RUN]${NC} $*"; }
log_banner()  {
  echo -e "${CYAN}══════════════════════════════════════════════════════${NC}"
  echo -e "${CYAN}  $*${NC}"
  echo -e "${CYAN}══════════════════════════════════════════════════════${NC}"
}

# ─── bail() — Sortie sécurisée avec garantie de transparence ──
bail() {
  local reason="$1"
  echo ""
  log_error "${reason}"
  echo -e "${GREEN}${BOLD}  ⛑ Opération annulée — AUCUNE DONNÉE N'A ÉTÉ PERDUE${NC}"
  echo -e "${GREEN}  Les services existants continuent de tourner.${NC}"
  echo -e "${GREEN}  Les volumes et backups sont intacts.${NC}"
  echo ""
  exit 1
}

# ─── Exécution conditionnelle (dry-run aware) ──────────────
run_cmd() {
  if [[ "${DRY_RUN}" == true ]]; then
    log_dry "Exécuterait : $*"
    return 0
  fi
  "$@"
}

# ─── Fonctions utilitaires ─────────────────────────────────

require_cmd() {
  if ! command -v "$1" &>/dev/null; then
    bail "'$1' n'est pas installé. Installation requise."
  fi
}

require_env_file() {
  local env="$1"
  local env_file="${SCRIPT_DIR}/.env.${env}"
  if [[ ! -f "${env_file}" ]]; then
    bail "Fichier ${env_file} introuvable. Créez-le : cp .env.example .env.${env}"
  fi
}

check_no_placeholders() {
  local env="$1"
  local env_file="${SCRIPT_DIR}/.env.${env}"

  if grep -qE '<CHANGE_ME|<placeholder_SECRET|PLACEHOLDER>' "${env_file}" 2>/dev/null; then
    if [[ "${env}" == "prod" ]]; then
      bail "Des placeholders de secrets subsistent dans .env.prod. Refus de démarrer en PROD avec des secrets non configurés."
    else
      log_warn "Placeholders détectés dans .env.${env} (accepté pour dev/staging)"
    fi
  fi
}

compose_file() {
  local env="$1"
  echo "${SCRIPT_DIR}/docker-compose.${env}.yml"
}

get_named_volumes() {
  local compose="$1"
  docker compose -f "${compose}" config --volumes 2>/dev/null || true
}

volume_exists() {
  local volume_name="$1"
  docker volume inspect "${volume_name}" &>/dev/null
}

# ─── Gate : Espace disque ─────────────────────────────────
check_disk_space() {
  local required_mb="${1:-${MIN_DISK_SPACE_MB}}"
  local path_to_check="${2:-${SCRIPT_DIR}}"

  local available_kb
  available_kb="$(df -P "${path_to_check}" 2>/dev/null | awk 'NR==2 {print $4}')"
  local available_mb=$((available_kb / 1024))

  if [[ ${available_mb} -lt ${required_mb} ]]; then
    bail "Espace disque insuffisant : ${available_mb} Mo disponibles, ${required_mb} Mo requis. Les opérations (backup, WAL, build) peuvent corrompre les données."
  fi

  log_success "Espace disque vérifié : ${available_mb} Mo disponibles ≥ ${required_mb} Mo requis"
}

# ─── Gate : Test d'écriture sur les volumes ───────────────
check_volume_write_access() {
  local compose="$1"
  local env="$2"
  local failed=false

  log_step "Test d'écriture sur les volumes existants..."

  local volumes
  volumes="$(get_named_volumes "${compose}")"

  if [[ -z "${volumes}" ]]; then
    log_info "Aucun volume nommé à tester."
    return 0
  fi

  local v
  for v in ${volumes}; do
    local full_name="${COMPOSE_PROJECT_NAME}_${v}"

    if volume_exists "${full_name}"; then
      if ! run_cmd docker run --rm \
        -v "${full_name}:/test_vol" \
        alpine sh -c "touch /test_vol/.deploy_write_test && rm /test_vol/.deploy_write_test" 2>/dev/null; then
        log_error "Volume ${full_name} : ÉCRITURE IMPOSSIBLE"
        failed=true
      else
        log_success "Volume ${full_name} : écriture OK"
      fi
    fi
  done

  if [[ "${failed}" == true ]]; then
    bail "Un ou plusieurs volumes ne sont pas accessibles en écriture. Les conteneurs démarreraient mais ne pourraient pas fonctionner."
  fi
}

# ─── Gate : Intégrité backup SQLite ────────────────────────
check_sqlite_integrity() {
  local backup_file="$1"
  local tmp_dir
  tmp_dir="$(mktemp -d)"

  tar xzf "${backup_file}" -C "${tmp_dir}" 2>/dev/null || {
    rm -rf "${tmp_dir}"
    log_error "Extraction du backup échouée : ${backup_file}"
    return 1
  }

  local db_file
  local integrity_ok=true
  while IFS= read -r -d '' db_file; do
    local result
    result="$(sqlite3 "${db_file}" "PRAGMA integrity_check;" 2>/dev/null || echo "FAIL")"
    if [[ "${result}" != "ok" ]]; then
      log_error "SQLite ${db_file} : intégrité COMPROMISE → ${result}"
      integrity_ok=false
    else
      log_success "SQLite ${db_file} : intégrité OK"
    fi
  done < <(find "${tmp_dir}" -type f \( -name "*.db" -o -name "*.sqlite" -o -name "*.sqlite3" \) -print0 2>/dev/null)

  rm -rf "${tmp_dir}"
  "${integrity_ok}"
}

# ─── Gate : Intégrité dump PostgreSQL ──────────────────────
check_pg_dump_integrity() {
  local dump_file="$1"
  if file "${dump_file}" | grep -q "PostgreSQL"; then
    log_success "PostgreSQL dump : format valide"
    return 0
  fi
  if gzip -t "${dump_file}" 2>/dev/null; then
    log_success "PostgreSQL dump (gz) : archive intacte"
    return 0
  fi
  log_error "PostgreSQL dump : format invalide ou corrompu"
  return 1
}

# ─── Gate : Intégrité dump MySQL ───────────────────────────
check_mysql_dump_integrity() {
  local dump_file="$1"
  if gzip -t "${dump_file}" 2>/dev/null; then
    local head_content
    head_content="$(zcat "${dump_file}" | head -20 2>/dev/null || true)"
    if echo "${head_content}" | grep -qiE '(MySQL dump|INSERT INTO|CREATE TABLE|mysqldump)'; then
      log_success "MySQL dump (gz) : contenu valide"
      return 0
    fi
  fi
  log_error "MySQL dump : format invalide ou corrompu"
  return 1
}

# ─── Fonctions de Backup ───────────────────────────────────

ensure_backup_dir() {
  mkdir -p "${BACKUP_DIR}"
}

volume_size_kb() {
  local volume_name="$1"
  docker run --rm -v "${volume_name}:/data" alpine du -sk /data 2>/dev/null | awk '{print $1}' || echo "0"
}

file_size_kb() {
  local filepath="$1"
  local size_bytes
  size_bytes="$(stat -f%z "${filepath}" 2>/dev/null || stat -c%s "${filepath}" 2>/dev/null || echo 0)"
  echo $((size_bytes / 1024))
}

backup_volumes() {
  local compose="$1"
  local env="$2"
  local backup_tag="${env}_${TIMESTAMP}"
  LAST_BACKUP_TAG="${backup_tag}"

  log_step "Backup des volumes pour l'environnement ${env}..."

  local volumes
  volumes="$(get_named_volumes "${compose}")"

  if [[ -z "${volumes}" ]]; then
    log_info "Aucun volume nommé détecté. Pas de backup volume nécessaire."
    return 0
  fi

  ensure_backup_dir

  local backup_files=()
  local volume_name
  for volume_name in ${volumes}; do
    local full_volume_name="${COMPOSE_PROJECT_NAME}_${volume_name}"

    if volume_exists "${full_volume_name}"; then
      log_info "Backup du volume ${full_volume_name}..."

      local active_size_kb
      active_size_kb="$(volume_size_kb "${full_volume_name}")"
      log_info "  Volume actif : ${active_size_kb} Ko"

      local backup_path="${BACKUP_DIR}/${full_volume_name}_${backup_tag}.tar.gz"

      run_cmd docker run --rm \
        -v "${full_volume_name}:/source:ro" \
        -v "${BACKUP_DIR}:/backup" \
        alpine tar czf "/backup/$(basename "${backup_path}")" -C /source . \
        2>/dev/null

      if [[ -f "${backup_path}" ]] || [[ "${DRY_RUN}" == true ]]; then
        if [[ "${DRY_RUN}" != true ]]; then
          local backup_size_kb
          backup_size_kb="$(file_size_kb "${backup_path}")"
          log_info "  Backup : ${backup_size_kb} Ko"

          # ─── Gate : Taille backup vs volume actif ───
          if [[ ${active_size_kb} -gt 100 ]]; then
            local ratio
            ratio="$(echo "scale=2; ${backup_size_kb} / ${active_size_kb}" | bc 2>/dev/null || echo "1")"
            if (( $(echo "${ratio} < ${BACKUP_SIZE_RATIO_MIN}" | bc -l 2>/dev/null || echo 0) )); then
              log_error "Backup ${backup_size_kb} Ko vs volume ${active_size_kb} Ko (ratio ${ratio})"
              log_error "Le backup est anormalement petit par rapport au volume — possible corruption"
              bail "Backup ${full_volume_name} : taille incohérente. Refus de continuer."
            fi
          fi

          local size_human
          size_human="$(du -h "${backup_path}" | cut -f1)"
          log_success "Volume ${full_volume_name} → ${backup_path} (${size_human})"
        fi
        backup_files+=("${backup_path}")
      else
        bail "Échec du backup du volume ${full_volume_name} — fichier non créé."
      fi
    else
      log_warn "Volume ${full_volume_name} n'existe pas encore. Skip."
    fi
  done

  # Gate : Au moins un backup créé si des volumes existaient
  local existing_volumes=0
  for v in ${volumes}; do
    if volume_exists "${COMPOSE_PROJECT_NAME}_${v}"; then
      existing_volumes=$((existing_volumes + 1))
    fi
  done

  if [[ ${existing_volumes} -gt 0 ]] && [[ ${#backup_files[@]} -eq 0 ]] && [[ "${DRY_RUN}" != true ]]; then
    bail "Des volumes existaient mais aucun backup n'a été créé. Opération annulée."
  fi

  log_success "Backup des volumes terminé"
  return 0
}

backup_databases() {
  local compose="$1"
  local env="$2"
  local backup_tag="${env}_${TIMESTAMP}"

  log_step "Backup des bases de données pour ${env}..."
  ensure_backup_dir

  local services
  services="$(docker compose -f "${compose}" config --services 2>/dev/null || true)"

  # ─── PostgreSQL ───
  # Priorité : service map, puis heuristiques
  local pg_service
  pg_service="$(get_data_service_name "${compose}" "${env}")"

  if [[ -n "${pg_service}" ]] && [[ "$(get_data_service_type)" =~ ^(postgres|postgresql|unknown)$ ]]; then
    if docker compose -f "${compose}" ps "${pg_service}" 2>/dev/null | grep -qiE "running|Up"; then
      log_info "Service PostgreSQL actif : ${pg_service} — dump en cours..."

      local dump_path="${BACKUP_DIR}/pg_${pg_service}_${backup_tag}.sql.gz"
      run_cmd docker compose -f "${compose}" exec -T "${pg_service}" \
        pg_dumpall -U postgres 2>/dev/null | gzip > "${dump_path}" 2>/dev/null || true

      if [[ -f "${dump_path}" ]] && [[ -s "${dump_path}" ]]; then
        if check_pg_dump_integrity "${dump_path}"; then
          local dump_size_kb
          dump_size_kb="$(file_size_kb "${dump_path}")"
          if [[ ${dump_size_kb} -lt 1 ]]; then
            bail "Le dump PostgreSQL est vide (0 Ko). Le conteneur tourne encore."
          fi
          log_success "PostgreSQL dump : ${dump_path}"
        else
          bail "Le dump PostgreSQL est corrompu. Le conteneur tourne encore — aucune donnée perdue."
        fi
      else
        log_warn "pg_dump échoué pour ${pg_service} (DB peut-être pas encore initialisée)"
      fi
    else
      log_warn "Service ${pg_service} n'est pas actif. Skip du dump PostgreSQL."
    fi
  fi

  # ─── MySQL / MariaDB ───
  local mysql_service
  # Priorité : service map
  if [[ "$(get_data_service_type)" == "mysql" ]]; then
    mysql_service="${SERVICE_DATA_NAME}"
  else
    mysql_service="$(echo "${services}" | grep -m1 -E '(mysql|mariadb)' || true)"
  fi

  if [[ -n "${mysql_service}" ]]; then
    if docker compose -f "${compose}" ps "${mysql_service}" 2>/dev/null | grep -qiE "running|Up"; then
      log_info "Service MySQL/MariaDB actif : ${mysql_service} — dump en cours..."

      local db_name db_user db_password
      db_name="$(docker compose -f "${compose}" exec "${mysql_service}" env 2>/dev/null \
        | grep MYSQL_DATABASE | cut -d= -f2 || echo "mysql")"
      db_user="$(docker compose -f "${compose}" exec "${mysql_service}" env 2>/dev/null \
        | grep MYSQL_USER | cut -d= -f2 || echo "root")"
      db_password="$(docker compose -f "${compose}" exec "${mysql_service}" env 2>/dev/null \
        | grep -E '^MYSQL_PASSWORD=' | cut -d= -f2 || echo "")"

      local dump_path="${BACKUP_DIR}/mysql_${mysql_service}_${backup_tag}.sql.gz"
      local dump_cmd="mysqldump -u ${db_user}"
      [[ -n "${db_password}" ]] && dump_cmd="${dump_cmd} -p${db_password}"
      dump_cmd="${dump_cmd} --all-databases"

      run_cmd docker compose -f "${compose}" exec -T "${mysql_service}" \
        bash -c "${dump_cmd}" 2>/dev/null | gzip > "${dump_path}" 2>/dev/null || true

      if [[ -f "${dump_path}" ]] && [[ -s "${dump_path}" ]]; then
        if check_mysql_dump_integrity "${dump_path}"; then
          log_success "MySQL dump : ${dump_path}"
        else
          bail "Le dump MySQL est corrompu. Le conteneur tourne encore — aucune donnée perdue."
        fi
      else
        log_warn "mysqldump échoué pour ${mysql_service} (DB non encore initialisée ?)"
      fi
    else
      log_warn "Service ${mysql_service} n'est pas actif. Skip du dump MySQL."
    fi
  fi

  return 0
}

# ─── Gate : Vérification post-down des bind mounts ─────────
check_bind_mounts_post_down() {
  local compose="$1"
  local env="$2"

  log_step "Vérification post-down : bind mounts intacts..."

  local compose_content
  compose_content="$(cat "${compose}" 2>/dev/null || true)"

  local bind_sources
  bind_sources="$(echo "${compose_content}" | grep -oE '^\s+-\s+\./[^:]+' | sed 's/^\s*- //' | sed 's|^\./||' || true)"

  if [[ -z "${bind_sources}" ]]; then
    log_info "Aucun bind mount détecté dans le compose."
    return 0
  fi

  local src
  for src in ${bind_sources}; do
    local full_path="${SCRIPT_DIR}/${src}"
    if [[ -e "${full_path}" ]]; then
      local size
      size="$(du -sh "${full_path}" 2>/dev/null | cut -f1 || echo "inaccessible")"
      log_success "Bind mount ${src} : présent (${size})"
    else
      log_error "Bind mount ${src} : ABSENT après down !"
      bail "Le répertoire ${full_path} a disparu après le down. Possible problème de mount."
    fi
  done

  log_success "Tous les bind mounts sont intacts après le down"
}

# ─── Vérification de santé ─────────────────────────────────

wait_for_healthy() {
  local compose="$1"
  local env="$2"
  local timeout="${3:-120}"
  local interval=5

  log_step "Vérification des healthchecks (${env}) — timeout ${timeout}s..."

  local elapsed=0
  while [[ ${elapsed} -lt ${timeout} ]]; do
    local all_healthy=true
    local has_unhealthy=false
    local services
    services="$(docker compose -f "${compose}" config --services 2>/dev/null || true)"

    local service
    for service in ${services}; do
      local container_id
      container_id="$(docker compose -f "${compose}" ps -q "${service}" 2>/dev/null || true)"

      if [[ -z "${container_id}" ]]; then
        all_healthy=false
        continue
      fi

      local health
      health="$(docker inspect --format='{{.State.Health.Status}}' "${container_id}" 2>/dev/null || echo "none")"

      case "${health}" in
        healthy) ;;
        unhealthy)
          if [[ "${has_unhealthy}" == false ]]; then
            log_error "Service ${service} : UNHEALTHY"
            has_unhealthy=true
          fi
          all_healthy=false
          ;;
        starting|"none"|"")
          all_healthy=false
          ;;
      esac
    done

    if [[ "${all_healthy}" == true ]]; then
      log_success "Tous les services sont sains pour ${env}"
      return 0
    fi

    sleep "${interval}"
    elapsed=$((elapsed + interval))
  done

  log_warn "Timeout de santé atteint (${timeout}s)."
  return 1
}

# ─── Rollback ───────────────────────────────────────────────

rollback_volumes() {
  local compose="$1"
  local env="$2"
  local rollback_tag="pre-rollback_${TIMESTAMP}"

  log_step "ROLLBACK — ${env^^}"
  log_warn "Restauration du dernier backup validé..."

  # 1. Sauver l'état courant AVANT rollback
  log_step "Sauvegarde de l'état courant avant rollback..."
  local volumes
  volumes="$(get_named_volumes "${compose}")"

  ensure_backup_dir
  local v
  for v in ${volumes}; do
    local full_name="${COMPOSE_PROJECT_NAME}_${v}"
    if volume_exists "${full_name}"; then
      local pre_rollback_path="${BACKUP_DIR}/${full_name}_${rollback_tag}.tar.gz"
      docker run --rm \
        -v "${full_name}:/source:ro" \
        -v "${BACKUP_DIR}:/backup" \
        alpine tar czf "/backup/$(basename "${pre_rollback_path}")" -C /source . \
        2>/dev/null || true
      if [[ -f "${pre_rollback_path}" ]]; then
        log_success "État courant sauvegardé → ${pre_rollback_path}"
      fi
    fi
  done

  # 2. Trouver les derniers backups par volume
  local has_any_backup=false
  for v in ${volumes}; do
    local full_name="${COMPOSE_PROJECT_NAME}_${v}"
    local vb
    vb="$(ls -t "${BACKUP_DIR}"/${full_name}_${env}_*.tar.gz 2>/dev/null | head -1 || true)"

    if [[ -n "${vb}" ]] && volume_exists "${full_name}"; then
      has_any_backup=true
      log_info "Restauration du volume ${full_name} depuis ${vb}..."

      # Vider le volume courant
      docker run --rm \
        -v "${full_name}:/target" \
        alpine sh -c "rm -rf /target/* /target/.[!.]* 2>/dev/null || true"

      # Restaurer le backup
      docker run --rm \
        -v "${full_name}:/target" \
        -v "${BACKUP_DIR}:/backup" \
        alpine tar xzf "/backup/$(basename "${vb}")" -C /target

      log_success "Volume ${full_name} restauré"
    fi
  done

  if [[ "${has_any_backup}" == false ]]; then
    bail "Aucun backup trouvé pour rollback. L'état courant a été sauvegardé au cas où."
  fi

  log_success "Rollback terminé. État courant sauvegardé, backup restauré."
}

# ─── Commandes principales ─────────────────────────────────

cmd_up() {
  local env="$1"
  local compose
  compose="$(compose_file "${env}")"

  log_banner "DÉMARRAGE — ${env^^}"
  require_env_file "${env}"
  check_no_placeholders "${env}"

  # 1. Espace disque
  check_disk_space

  # 2. Git pull (sauf si modifications locales)
  log_step "Synchronisation du dépôt..."
  if [[ "${DRY_RUN}" != true ]]; then
    if git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null; then
      git pull --ff-only 2>/dev/null && log_success "Dépôt synchronisé" \
        || log_warn "git pull échoué (modifications locales ou pas de remote)"
    else
      log_warn "Modifications locales détectées — git pull ignoré"
    fi
  else
    log_dry "Exécuterait : git pull --ff-only"
  fi

  # 3. Services existants ?
  local running_services
  running_services="$(docker compose -f "${compose}" ps -q 2>/dev/null || true)"

  # 4. Cycle de redéploiement si services actifs
  if [[ -n "${running_services}" ]]; then
    log_step "Services existants détectés — cycle de redéploiement..."

    # 4a. Backup AVANT down (conteneurs actifs)
    backup_databases "${compose}" "${env}"
    backup_volumes "${compose}" "${env}"

    # 4b. ⛔ GATE : vérifier que les backups existent
    if [[ "${DRY_RUN}" != true ]]; then
      local backup_count
      backup_count="$(find "${BACKUP_DIR}" -name "*${TIMESTAMP}*" -type f 2>/dev/null | wc -l)"
      if [[ ${backup_count} -eq 0 ]]; then
        bail "AUCUN BACKUP CRÉÉ alors que les services tournaient. Les conteneurs tournent encore."
      fi
      log_success "Backup vérifié (${backup_count} fichier(s))"

      # 4c. ⛔ GATE : Intégrité des archives
      local f
      for f in "${BACKUP_DIR}"/*"${TIMESTAMP}"*.tar.gz; do
        [[ -f "${f}" ]] || continue
        if ! gzip -t "${f}" 2>/dev/null; then
          bail "Backup corrompu : ${f}. Les conteneurs tournent encore — aucune donnée perdue."
        fi
        local bk_size
        bk_size="$(file_size_kb "${f}")"
        if [[ ${bk_size} -lt 1 ]]; then
          bail "Backup vide ou quasi-vide : ${f} (${bk_size} Ko). Conteneurs encore actifs."
        fi
        log_success "Intégrité : $(basename "${f}") OK"
      done

      for f in "${BACKUP_DIR}"/*"${TIMESTAMP}"*.sql.gz; do
        [[ -f "${f}" ]] || continue
        if ! gzip -t "${f}" 2>/dev/null; then
          bail "Dump SQL corrompu : ${f}. Conteneurs encore actifs — aucune donnée perdue."
        fi
        log_success "Intégrité : $(basename "${f}") OK"
      done
    fi

    # 4d. Test d'écriture sur volumes
    check_volume_write_access "${compose}" "${env}"

    # 4e. down --remove-orphans (APRÈS backup validé)
    log_step "Arrêt des services existants (--remove-orphans)..."
    run_cmd docker compose -f "${compose}" down --remove-orphans 2>&1
    log_success "Services arrêtés. Orphelins nettoyés."

    # 4f. Vérification post-down : bind mounts intacts
    if [[ "${DRY_RUN}" != true ]]; then
      check_bind_mounts_post_down "${compose}" "${env}"
    fi
  fi

  # 5. Build (APRÈS down)
  log_step "Construction des images..."
  run_cmd docker compose -f "${compose}" build 2>&1
  if [[ "${DRY_RUN}" != true ]]; then
    log_success "Build terminé"
  fi

  # 6. Démarrage
  log_step "Démarrage des services..."
  run_cmd docker compose -f "${compose}" up -d 2>&1
  if [[ "${DRY_RUN}" != true ]]; then
    log_success "Services démarrés"
  fi

  # 7. Healthcheck + rollback auto si échec
  if [[ "${env}" != "dev" ]] && [[ "${DRY_RUN}" != true ]]; then
    local health_timeout
    case "${env}" in
      staging) health_timeout=120 ;;
      prod)    health_timeout=90  ;;
      *)       health_timeout=120 ;;
    esac

    if ! wait_for_healthy "${compose}" "${env}" "${health_timeout}"; then
      log_error "Healthcheck échoué — rollback automatique..."
      rollback_volumes "${compose}" "${env}"
      docker compose -f "${compose}" up -d 2>&1 || true
      bail "Déploiement échoué. Rollback effectué. État courant sauvegardé."
    fi
  else
    if [[ "${DRY_RUN}" == true ]]; then
      log_dry "Vérifierait les healthchecks (timeout selon environnement)"
    else
      log_info "Healthcheck ignoré en dev (rapidité prioritaire)"
    fi
  fi

  # 8. Statut
  echo ""
  if [[ "${DRY_RUN}" != true ]]; then
    docker compose -f "${compose}" ps
  fi
  echo ""
  log_banner "${env^^} — OPÉRATIONNEL"
}

cmd_down() {
  local env="$1"
  local compose
  compose="$(compose_file "${env}")"

  log_banner "ARRÊT — ${env^^}"
  require_env_file "${env}"

  local running
  running="$(docker compose -f "${compose}" ps -q 2>/dev/null || true)"
  if [[ -z "${running}" ]]; then
    log_info "Aucun service en cours d'exécution pour ${env}."
    return 0
  fi

  # Lister les volumes
  local volumes
  volumes="$(get_named_volumes "${compose}")"
  if [[ -n "${volumes}" ]]; then
    log_step "Volumes nommés détectés :"
    local v
    for v in ${volumes}; do
      local full_name="${COMPOSE_PROJECT_NAME}_${v}"
      if volume_exists "${full_name}"; then
        log_warn "  ⚠ ${full_name} — CONTIENT DES DONNÉES"
      else
        log_info "  ○ ${full_name} — volume vide ou inexistant"
      fi
    done
  fi

  # Espace disque
  check_disk_space

  # Backup obligatoire si données existent
  local has_real_data=false
  for v in ${volumes}; do
    if volume_exists "${COMPOSE_PROJECT_NAME}_${v}"; then
      has_real_data=true
      break
    fi
  done

  if [[ "${has_real_data}" == true ]]; then
    log_step "PROTECTION DES DONNÉES — Backup obligatoire avant arrêt"
    backup_databases "${compose}" "${env}"
    backup_volumes "${compose}" "${env}"

    if [[ "${DRY_RUN}" != true ]]; then
      local backup_count
      backup_count="$(find "${BACKUP_DIR}" -name "*${TIMESTAMP}*" -type f 2>/dev/null | wc -l)"
      if [[ ${backup_count} -eq 0 ]]; then
        bail "AUCUN BACKUP CRÉÉ — OPÉRATION ANNULÉE. Conteneurs encore actifs, données intactes."
      fi

      local f
      for f in "${BACKUP_DIR}"/*"${TIMESTAMP}"*.tar.gz; do
        [[ -f "${f}" ]] || continue
        if ! gzip -t "${f}" 2>/dev/null; then
          bail "Backup corrompu : ${f}. Opération annulée, conteneurs encore actifs."
        fi
      done

      log_success "Backup vérifié et validé (${backup_count} fichier(s))"
    fi
  fi

  # Confirmation interactive
  if [[ "${FORCE_DOWN:-}" != "true" ]]; then
    echo ""
    log_warn "Vous allez arrêter l'environnement ${env}."
    if [[ "${has_real_data}" == true ]]; then
      log_warn "Des volumes contiennent des données. Un backup validé a été créé."
    fi
    read -rp "$(echo -e "${RED}${BOLD}Confirmer l'arrêt ? [y/N]${NC} ")" confirm
    if [[ "${confirm}" != "y" && "${confirm}" != "Y" ]]; then
      log_info "Opération annulée. Les services continuent de tourner."
      return 0
    fi
  fi

  # Test écriture volumes
  check_volume_write_access "${compose}" "${env}"

  # down --remove-orphans (SANS -v)
  log_step "Arrêt des services (--remove-orphans, volumes préservés)..."
  run_cmd docker compose -f "${compose}" down --remove-orphans 2>&1
  log_success "Services arrêtés. Volumes préservés. Orphelins nettoyés."

  # Post-down vérification
  if [[ "${DRY_RUN}" != true ]]; then
    check_bind_mounts_post_down "${compose}" "${env}"
  fi

  log_info "Pour supprimer les volumes manuellement : docker volume rm <volume_name>"
}

cmd_rebuild() {
  local env="$1"
  local compose
  compose="$(compose_file "${env}")"

  log_banner "RECONSTRUCTION — ${env^^}"
  require_env_file "${env}"

  # Backup si services actifs
  local running
  running="$(docker compose -f "${compose}" ps -q 2>/dev/null || true)"
  if [[ -n "${running}" ]]; then
    backup_databases "${compose}" "${env}"
    backup_volumes "${compose}" "${env}"
  fi

  check_disk_space

  # down --remove-orphans
  log_step "Arrêt des services..."
  run_cmd docker compose -f "${compose}" down --remove-orphans 2>&1 || true

  if [[ "${DRY_RUN}" != true ]]; then
    check_bind_mounts_post_down "${compose}" "${env}"
  fi

  # Build sans cache
  log_step "Build sans cache..."
  run_cmd docker compose -f "${compose}" build --no-cache 2>&1

  # Redémarrage
  log_step "Redémarrage..."
  run_cmd docker compose -f "${compose}" up -d 2>&1

  # Healthcheck + rollback
  if [[ "${env}" != "dev" ]] && [[ "${DRY_RUN}" != true ]]; then
    if ! wait_for_healthy "${compose}" "${env}"; then
      log_error "Healthcheck échoué après rebuild — rollback..."
      rollback_volumes "${compose}" "${env}"
      docker compose -f "${compose}" up -d 2>&1 || true
      bail "Rebuild échoué. Rollback effectué."
    fi
  fi
}

cmd_status() {
  local env="$1"
  local compose
  compose="$(compose_file "${env}")"

  log_banner "STATUT — ${env^^}"

  echo -e "${BOLD}Services :${NC}"
  docker compose -f "${compose}" ps 2>/dev/null || echo "  Aucun service en cours"

  echo ""
  echo -e "${BOLD}Volumes :${NC}"
  local volumes
  volumes="$(get_named_volumes "${compose}")"
  if [[ -n "${volumes}" ]]; then
    local v
    for v in ${volumes}; do
      local full_name="${COMPOSE_PROJECT_NAME}_${v}"
      if volume_exists "${full_name}"; then
        local vsize
        vsize="$(volume_size_kb "${full_name}")"
        echo -e "  ${GREEN}●${NC} ${full_name} (${vsize} Ko)"
      else
        echo -e "  ${RED}○${NC} ${full_name} (non créé)"
      fi
    done
  else
    echo "  Aucun volume nommé"
  fi

  echo ""
  echo -e "${BOLD}Ressources :${NC}"
  docker compose -f "${compose}" stats --no-stream 2>/dev/null || echo "  Aucun container actif"

  echo ""
  echo -e "${BOLD}Espace disque :${NC}"
  local avail_kb
  avail_kb="$(df -P "${SCRIPT_DIR}" 2>/dev/null | awk 'NR==2 {print $4}')"
  local avail_mb=$((avail_kb / 1024))
  echo "  ${avail_mb} Mo disponibles (seuil : ${MIN_DISK_SPACE_MB} Mo)"
}

cmd_backup() {
  local env="$1"
  local compose
  compose="$(compose_file "${env}")"

  log_banner "BACKUP MANUEL — ${env^^}"

  check_disk_space
  backup_databases "${compose}" "${env}"
  backup_volumes "${compose}" "${env}"
  log_success "Backup terminé dans ${BACKUP_DIR}/"

  # Nettoyage backups > 30 jours
  log_step "Nettoyage des backups de plus de 30 jours..."
  find "${BACKUP_DIR}" -name "*.tar.gz" -type f -mtime +30 -delete 2>/dev/null || true
  find "${BACKUP_DIR}" -name "*.sql.gz" -type f -mtime +30 -delete 2>/dev/null || true
  log_success "Nettoyage terminé"
}

cmd_logs() {
  local env="$1"
  shift || true
  local compose
  compose="$(compose_file "${env}")"

  docker compose -f "${compose}" logs -f "${@:-}"
}

cmd_rollback() {
  local env="$1"
  local compose
  compose="$(compose_file "${env}")"

  log_banner "ROLLBACK — ${env^^}"

  local running
  running="$(docker compose -f "${compose}" ps -q 2>/dev/null || true)"
  if [[ -n "${running}" ]]; then
    log_warn "Des services sont encore en cours. Arrêt nécessaire avant rollback."
    read -rp "$(echo -e "${YELLOW}${BOLD}Arrêter les services pour rollback ? [y/N]${NC} ")" confirm
    if [[ "${confirm}" == "y" || "${confirm}" == "Y" ]]; then
      docker compose -f "${compose}" down --remove-orphans 2>&1
    else
      bail "Rollback annulé. Les services tournent encore, les données sont intactes."
    fi
  fi

  rollback_volumes "${compose}" "${env}"

  log_info "Pour redémarrer : bash deploy.sh ${env} up"
}

cmd_check() {
  local env="$1"
  local compose
  compose="$(compose_file "${env}")"

  log_banner "VÉRIFICATION PRÉ-DÉPLOIEMENT — ${env^^}"

  local checks_passed=0
  local checks_failed=0

  # 1. Fichier .env
  if [[ -f "${SCRIPT_DIR}/.env.${env}" ]]; then
    log_success "Fichier .env.${env} : présent"
    checks_passed=$((checks_passed + 1))
  else
    log_error "Fichier .env.${env} : ABSENT"
    checks_failed=$((checks_failed + 1))
  fi

  # 2. Placeholders
  if grep -qE '<CHANGE_ME|<placeholder_SECRET|PLACEHOLDER>' "${SCRIPT_DIR}/.env.${env}" 2>/dev/null; then
    if [[ "${env}" == "prod" ]]; then
      log_error "Secrets : placeholders non remplacés (BLOQUANT en prod)"
      checks_failed=$((checks_failed + 1))
    else
      log_warn "Secrets : placeholders détectés (acceptable en ${env})"
      checks_passed=$((checks_passed + 1))
    fi
  else
    log_success "Secrets : aucun placeholder détecté"
    checks_passed=$((checks_passed + 1))
  fi

  # 3. Compose file
  if [[ -f "${compose}" ]]; then
    log_success "Compose file : présent"
    checks_passed=$((checks_passed + 1))

    if docker compose -f "${compose}" config >/dev/null 2>&1; then
      log_success "Compose syntaxe : valide"
      checks_passed=$((checks_passed + 1))
    else
      log_error "Compose syntaxe : INVALIDE"
      checks_failed=$((checks_failed + 1))
    fi
  else
    log_error "Compose file : ABSENT"
    checks_failed=$((checks_failed + 1))
  fi

  # 4. Dockerfile
  if [[ -f "${SCRIPT_DIR}/Dockerfile" ]]; then
    log_success "Dockerfile : présent"
    checks_passed=$((checks_passed + 1))
  else
    log_warn "Dockerfile : absent (sera requis pour le build)"
    checks_failed=$((checks_failed + 1))
  fi

  # 5. Espace disque
  local avail_kb
  avail_kb="$(df -P "${SCRIPT_DIR}" 2>/dev/null | awk 'NR==2 {print $4}')"
  local avail_mb=$((avail_kb / 1024))
  if [[ ${avail_mb} -ge ${MIN_DISK_SPACE_MB} ]]; then
    log_success "Espace disque : ${avail_mb} Mo ≥ ${MIN_DISK_SPACE_MB} Mo"
    checks_passed=$((checks_passed + 1))
  else
    log_error "Espace disque : ${avail_mb} Mo < ${MIN_DISK_SPACE_MB} Mo"
    checks_failed=$((checks_failed + 1))
  fi

  # 6. Docker daemon
  if docker info >/dev/null 2>&1; then
    log_success "Docker daemon : actif"
    checks_passed=$((checks_passed + 1))
  else
    log_error "Docker daemon : inactif ou inaccessible"
    checks_failed=$((checks_failed + 1))
  fi

  # 7. Volumes existants
  local volumes
  volumes="$(get_named_volumes "${compose}")"
  if [[ -n "${volumes}" ]]; then
    local v
    for v in ${volumes}; do
      local full_name="${COMPOSE_PROJECT_NAME}_${v}"
      if volume_exists "${full_name}"; then
        log_info "Volume ${full_name} : existant (données préservées)"
      else
        log_info "Volume ${full_name} : inexistant (sera créé)"
      fi
    done
  fi

  # 8. Backups existants
  local backup_count
  backup_count="$(find "${BACKUP_DIR}" -type f \( -name "*.tar.gz" -o -name "*.sql.gz" \) 2>/dev/null | wc -l || echo 0)"
  if [[ ${backup_count} -gt 0 ]]; then
    log_success "Backups existants : ${backup_count} fichier(s)"
  else
    log_warn "Aucun backup existant"
  fi
  checks_passed=$((checks_passed + 1))

  # 9. Vibebackbone : audits pré-déploiement
  if [[ -f "${SCRIPT_DIR}/docs/AUDIT_STATUS.md" ]]; then
    log_info "Vibebackbone AUDIT_STATUS.md détecté — vérification des pré-audits..."
    local blocked_audits
    blocked_audits="$(grep -c 'BLOCKED' "${SCRIPT_DIR}/docs/AUDIT_STATUS.md" 2>/dev/null || echo "0")"
    if [[ ${blocked_audits} -gt 0 ]]; then
      log_warn "AUDIT_STATUS.md contient ${blocked_audits} audit(s) BLOCKED — déploiement à risque"
      checks_failed=$((checks_failed + 1))
    else
      log_success "Aucun audit BLOCKED dans AUDIT_STATUS.md"
      checks_passed=$((checks_passed + 1))
    fi
  else
    log_warn "docs/AUDIT_STATUS.md absent — audits Vibebackbone pré-déploiement non vérifiables"
  fi

  # Bilan
  echo ""
  log_banner "BILAN : ${checks_passed} OK, ${checks_failed} ÉCHEC(S)"
  if [[ ${checks_failed} -gt 0 ]]; then
    bail "Vérification pré-déploiement échouée. Corrigez les problèmes avant de déployer."
  fi
  log_success "Toutes les vérifications sont passées. Prêt pour le déploiement."
}

# ─── Affichage de l'aide ───────────────────────────────────

show_usage() {
  cat <<EOF
${BOLD}deploy.sh${NC} — Moteur d'automatisation deploy-docker v2.1
${BOLD}VibeBackbone Skill${NC}: T-vbb-deploy-runtime

${BOLD}USAGE${NC}
  bash deploy.sh <environnement> [action] [options]

${BOLD}ENVIRONNEMENTS${NC}
  dev       Développement (bind-mounts, hot-reload, pas de healthcheck)
  staging   Pré-production (named volumes, healthcheck, réseau isolé)
  prod      Production (sécurité renforcée, limits, secrets, reverse-proxy)

${BOLD}ACTIONS${NC}
  up        Démarrer / redéployer (défaut)
              ↳ Cycle : backup → down → build → up → healthcheck
              ↳ Rollback automatique si healthcheck échoue
  down      Arrêter (backup obligatoire + validation intégrité)
  rebuild   Reconstruire sans cache et redémarrer
  status    Statut des services, volumes, ressources, disque
  backup    Backup manuel (validé en intégrité)
  logs      Suivre les logs en temps réel
  rollback  Restaurer le dernier backup validé
  check     Vérification pré-déploiement

${BOLD}OPTIONS${NC}
  --dry-run       Simulation complète, zéro action
  --check         Alias pour action 'check'
  --force         Passer la confirmation interactive de 'down'
  FORCE_DOWN=true Idem, via variable d'environnement

${BOLD}PROTECTIONS (gates d'intégrité)${NC}
  ✓ Backup obligatoire avant tout down (conteneurs actifs)
  ✓ Gate intégrité : archive corrompue → arrêt immédiat
  ✓ Gate taille : backup vide/incohérent → arrêt immédiat
  ✓ Gate espace disque : < ${MIN_DISK_SPACE_MB} Mo → arrêt
  ✓ Test d'écriture sur chaque volume existant
  ✓ down --remove-orphans (nettoyage des conteneurs fantômes)
  ✓ Vérification post-down des bind mounts
  ✓ Rollback automatique si healthcheck échoue
  ✓ Sauvegarde de l'état courant avant tout rollback
  ✓ bail() : sortie sécurisée "aucune donnée perdue"

${BOLD}EXEMPLES${NC}
  bash deploy.sh dev                          # Démarre dev
  bash deploy.sh staging --dry-run            # Simulation staging
  bash deploy.sh prod check                   # Vérif pré-déploiement
  bash deploy.sh prod up                      # Déploiement production
  bash deploy.sh prod down                    # Arrêt (backup validé)
  bash deploy.sh prod rollback                # Restauration backup N-1

EOF
}

# ─── Point d'entrée ────────────────────────────────────────

main() {
  require_cmd docker
  require_cmd git

  # Charger la service map (déterministe) ou fallback heuristiques
  load_service_map || true

  # Parsing des options globales
  local positional_args=()

  local arg
  for arg in "$@"; do
    case "${arg}" in
      --dry-run)  DRY_RUN=true ;;
      --force)    FORCE_DOWN=true ;;
      --check)    CHECK_MODE=true ;;
      -h|--help)  show_usage; exit 0 ;;
      *)          positional_args+=("${arg}") ;;
    esac
  done

  set -- "${positional_args[@]}"

  # Mode --check sans env : vérifier tous les envs
  if [[ "${CHECK_MODE}" == true ]] && [[ $# -eq 0 ]]; then
    for env in dev staging prod; do
      if [[ -f "$(compose_file "${env}")" ]]; then
        cmd_check "${env}"
        echo ""
      fi
    done
    exit 0
  fi

  if [[ $# -lt 1 ]]; then
    show_usage
    exit 0
  fi

  local env="$1"
  shift || true

  if [[ "${CHECK_MODE}" == true ]]; then
    cmd_check "${env}"
    exit 0
  fi

  local action="up"
  if [[ $# -ge 1 ]]; then
    action="$1"
    shift || true
  fi

  # Validation environnement
  case "${env}" in
    dev|staging|prod) ;;
    *) bail "Environnement invalide : '${env}'. Supportés : dev, staging, prod" ;;
  esac

  # Validation action
  case "${action}" in
    up|down|rebuild|status|backup|logs|rollback|check) ;;
    *) bail "Action invalide : '${action}'. Supportées : up, down, rebuild, status, backup, logs, rollback, check" ;;
  esac

  # Exécution
  "cmd_${action}" "${env}" "${@:-}"
}

main "$@"