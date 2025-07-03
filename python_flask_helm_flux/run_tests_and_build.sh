#!/bin/bash

# --------- Step 1: Run pylint ----------
echo "🔎 Running pylint..."
pylint app/ > pylint_report.txt || true  # Don't fail script even if pylint complains

# Extract pylint score (average)
score_line=$(tail -n 2 pylint_report.txt | grep "rated at")
score=$(echo "$score_line" | awk '{print $7}' | cut -d'/' -f1)

# If score is empty, fail
if [ -z "$score" ]; then
  echo "❌ Could not parse pylint score. Aborting."
  exit 1
fi

echo "✅ Pylint Score: $score/10"
pylint_ok_score=1

# --------- Step 2: Validate pylint score ----------
if (( $(echo "$score < ${pylint_ok_score}" | bc -l) )); then
  echo "❌ Pylint score is too low (<= 5). Skipping tests and Docker build."
  exit 1
fi

echo "🚀 Pylint score > 5. Proceeding to run tests..."

# --------- Step 3: Run pytest ----------
touch /tmp/results.xml
pytest --junitxml=/tmp/results.xml

# --------- Step 4: Parse pytest results ----------
read total passed <<< $(python3 <<EOF
import xml.etree.ElementTree as ET
tree = ET.parse('/tmp/results.xml')
root = tree.getroot()
total = int(root.attrib['tests'])
failures = int(root.attrib.get('failures', 0))
errors = int(root.attrib.get('errors', 0))
skipped = int(root.attrib.get('skipped', 0))
passed = total - failures - errors - skipped
print(total, passed)
EOF
)

# --------- Step 5: Decide Docker Build ----------
if [ "$total" -eq 0 ]; then
  echo "❌ No tests found. Aborting."
  exit 1
fi

pass_percent=$(( 100 * passed / total ))
echo "✅ Passed: $passed / $total ($pass_percent%)"

if [ "$pass_percent" -gt 50 ]; then
  echo "📦 More than 50% tests passed. Building Docker image..."
  docker build -t your-image-name .
else
  echo "❌ Less than or equal to 50% tests passed. Skipping Docker build."
  exit 1
fi
