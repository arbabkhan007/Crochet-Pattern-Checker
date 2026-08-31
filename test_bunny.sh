#!/bin/bash

echo "🧸 Testing Amigurumi Bunny Pattern"
echo "=================================="

PATTERN="examples/amigurumi_bunny.txt"

echo -e "\n1️⃣ VALIDATION"
echo "----------------"
crochet-check check $PATTERN

echo -e "\n2️⃣ AI EXPLANATION"
echo "--------------------"
crochet-check explain $PATTERN

echo -e "\n3️⃣ 2D VISUALIZATION"
echo "----------------------"
crochet-check render $PATTERN -o output/bunny/

echo -e "\n4️⃣ 3D SIMULATION"
echo "-------------------"
crochet-check render-3d $PATTERN -o output/bunny/

echo -e "\n5️⃣ PDF GENERATION (all templates)"
echo "------------------------------------"
for template in minimal craft modern ocean berry sunset; do
    echo "  Generating $template template..."
    crochet-check pdf $PATTERN --template $template -o output/bunny/bunny_$template.pdf
done

echo -e "\n6️⃣ COVER IMAGE"
echo "-----------------"
crochet-check image $PATTERN -o output/bunny/bunny_cover.svg

echo -e "\n✅ All tests complete!"
echo "Check output/bunny/ for results"
