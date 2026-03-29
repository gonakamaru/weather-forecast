# Select IDs of old files and assign them to a file.

TARGET_ORG="weather-forecast-dev"
DELETE_CANDIDATE_FILE_NAME="old_files.csv"

sf data query \
  --query "SELECT Id FROM ContentDocument WHERE CreatedDate < LAST_N_DAYS:45 ORDER BY CreatedDate ASC LIMIT 200" \
  --result-format csv \
  --target-org $TARGET_ORG > $DELETE_CANDIDATE_FILE_NAME