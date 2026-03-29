# Delete files according to the IDs in the file.

TARGET_ORG="weather-forecast-dev"
DELETE_CANDIDATE_FILE_NAME="old_files.csv"

sf data delete bulk \
  --sobject ContentDocument \
  --target-org $TARGET_ORG \
  --file $DELETE_CANDIDATE_FILE_NAME
