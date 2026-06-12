#!/bin/bash
echo "{" > cases/index.json
echo '  "version": "2.0",' >> cases/index.json
echo '  "lastUpdated": "'$(date -Iseconds)'",' >> cases/index.json
echo '  "specialties": {' >> cases/index.json

specialties=(cardiology dermatology endocrinology gastroenterology gynecology hematology infectious nephrology neurology pediatrics pulmonology surgery)
first=true
for spec in "${specialties[@]}"; do
  if [ -d "cases/$spec" ]; then
    count=$(find "cases/$spec" -name "*.json" | wc -l)
    if [ "$first" = true ]; then first=false; else echo "," >> cases/index.json; fi
    echo -n "    \"$spec\": {\"label\": \"$spec\", \"caseCount\": $count}" >> cases/index.json
  fi
done
echo "" >> cases/index.json
echo '  }' >> cases/index.json
echo '}' >> cases/index.json
echo "✅ Index built with $(find cases -name '*.json' | wc -l) total cases"
