#!/bin/bash
echo "{" > cases/index.json
echo '  "version": "3.0",' >> cases/index.json
echo '  "lastUpdated": "'$(date -Iseconds)'",' >> cases/index.json
echo '  "specialties": {' >> cases/index.json

first_spec=true
for spec_dir in cases/*/; do
  spec=$(basename "$spec_dir")
  [ "$spec" = "index.json" ] && continue
  
  if [ "$first_spec" = true ]; then first_spec=false; else echo "," >> cases/index.json; fi
  
  echo "    \"$spec\": {" >> cases/index.json
  
  first_level=true
  for level_dir in "$spec_dir"*/; do
    level=$(basename "$level_dir")
    
    if [ "$first_level" = true ]; then first_level=false; else echo "," >> cases/index.json; fi
    
    echo "      \"$level\": [" >> cases/index.json
    
    first_case=true
    for case_file in "$level_dir"*.json; do
      case_id=$(basename "$case_file" .json)
      title=$(python3 -c "import json; print(json.load(open('$case_file')).get('title','$case_id'))" 2>/dev/null || echo "$case_id")
      
      if [ "$first_case" = true ]; then first_case=false; else echo "," >> cases/index.json; fi
      
      echo "        {\"id\": \"$case_id\", \"title\": \"$title\", \"specialty\": \"$spec\", \"difficulty\": \"$level\", \"file\": \"$spec/$level/$case_id.json\"}" >> cases/index.json
    done
    
    echo "" >> cases/index.json
    echo -n "      ]" >> cases/index.json
  done
  
  echo "" >> cases/index.json
  echo -n "    }" >> cases/index.json
done

echo "" >> cases/index.json
echo '  }' >> cases/index.json
echo '}' >> cases/index.json

echo "Manifest built: $(grep -c '"id"' cases/index.json) cases"
