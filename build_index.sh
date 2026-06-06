#!/bin/bash

echo '{'
echo '  "version": "4.0.0",'
echo '  "last_updated": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'",'

# Count total cases
total=$(find cases -name "*.json" | wc -l)
echo '  "total_cases": '$total','

echo '  "cases_by_specialty": {'
first_specialty=true

# Function to process specialty
process_specialty() {
  local dir=$1
  local name=$2
  
  # Count by difficulty/branch
  local beginner=0 intermediate=0 advanced=0 branches=""
  
  # Check if has level subdirectories (beginner/intermediate/advanced)
  if ls "$dir/beginner"/*.json 2>/dev/null >/dev/null; then
    beginner=$(ls "$dir/beginner"/*.json 2>/dev/null | wc -l)
  fi
  if ls "$dir/intermediate"/*.json 2>/dev/null >/dev/null; then
    intermediate=$(ls "$dir/intermediate"/*.json 2>/dev/null | wc -l)
  fi
  if ls "$dir/advanced"/*.json 2>/dev/null >/dev/null; then
    advanced=$(ls "$dir/advanced"/*.json 2>/dev/null | wc -l)
  fi
  
  echo "    \"$name\": { \"beginner\": $beginner, \"intermediate\": $intermediate, \"advanced\": $advanced }"
}

# Process level-based specialties
specs=("cardiology" "pulmonology" "neurology" "endocrinology" "gastroenterology" "nephrology" "hematology" "infectious" "rheumatology" "dermatology")

for spec in "${specs[@]}"; do
  if [ -d "cases/$spec" ]; then
    if [ "$first_specialty" = false ]; then echo ","; fi
    process_specialty "cases/$spec" "$spec"
    first_specialty=false
  fi
done

# Process branch-based specialties (pediatrics, surgery, gynecology)
echo ","
process_specialty "cases/pediatrics" "pediatrics"
echo ","
process_specialty "cases/surgery" "surgery"
echo ","
process_specialty "cases/gynecology" "gynecology"

echo '  },'
echo '  "cases": ['

first_case=true
find cases -name "*.json" | sort | while read file; do
  # Extract specialty, difficulty/branch, and title
  rel_path="$file"
  dir=$(dirname "$rel_path")
  filename=$(basename "$rel_path" .json)
  
  # Determine specialty and difficulty
  specialty=$(echo "$dir" | cut -d'/' -f2)
  difficulty=$(echo "$dir" | cut -d'/' -f3)
  
  # Try to extract title from file
  title=""
  if [ -f "$file" ]; then
    title=$(grep -o '"title": "[^"]*"' "$file" | head -1 | cut -d'"' -f4)
  fi
  [ -z "$title" ] && title="$filename"
  
  # Generate ID
  id="${specialty}_${difficulty}_${filename}"
  
  if [ "$first_case" = false ]; then echo ","; fi
  echo -n "    {\"id\":\"$id\",\"title\":\"$title\",\"specialty\":\"$specialty\",\"difficulty\":\"$difficulty\",\"path\":\"$rel_path\"}"
  first_case=false
done

echo ''
echo '  ]'
echo '}'
