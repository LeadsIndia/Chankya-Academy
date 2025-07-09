import json

# --- Step 1: Generate 1500 Placeholder Questions ---

regions = [
    {"name": "North India", "count": 250},
    {"name": "South India", "count": 250},
    {"name": "East India", "count": 200},
    {"name": "West India", "count": 200},
    {"name": "Central India", "count": 200},
    {"name": "Northeast India", "count": 200}
]

all_questions = []

for region in regions:
    for i in range(1, region["count"] + 1):
        question = {
            "region": region["name"],
            "question": f"{region['name']} Sample Question {i}",
            "options": [f"Option A{i}", f"Option B{i}", f"Option C{i}", f"Option D{i}"],
            "answer": f"Option A{i}"
        }
        all_questions.append(question)

# Save questions to JSON file
with open("indian_geography_questions.json", "w", encoding="utf-8") as f:
    json.dump(all_questions, f, indent=2, ensure_ascii=False)

print("1500 placeholder questions generated in 'indian_geography_questions.json'.")

# --- Step 2: Generate HTML Quiz Page ---

html_code = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Indian Geography Quiz</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; }}
    .question {{ margin-bottom: 18px; }}
    #result {{ font-weight: bold; margin-top: 18px; }}
    button {{ margin-right: 10px; }}
  </style>
</head>
<body>
  <h2>Indian Geography Quiz (Region-wise)</h2>
  <form id="quizForm"></form>
  <button type="button" onclick="submitQuiz()">Submit</button>
  <button type="button" onclick="resetQuiz()">Reset</button>
  <div id="result"></div>
  <script>
    let allQuestions = [];
    let regions = ["North India", "South India", "East India", "West India", "Central India", "Northeast India"];
    let questionsByRegion = {{}};
    let previousQuiz = [];

    // Load questions from JSON
    fetch('indian_geography_questions.json')
      .then(response => response.json())
      .then(data => {{
        allQuestions = data;
        regions.forEach(region => {{
          questionsByRegion[region] = allQuestions.filter(q => q.region === region);
        }});
        resetQuiz();
      }});

    function shuffle(array) {{
      for (let i = array.length - 1; i > 0; i--) {{
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }}
      return array;
    }}

    function selectQuiz() {{
      let newQuiz = [];
      let repeats = 0;
      let previousSet = new Set(previousQuiz.map(q => q.question));
      regions.forEach(region => {{
        let regionQuestions = questionsByRegion[region].slice();
        shuffle(regionQuestions);
        let selected = [];
        for (let q of regionQuestions) {{
          if (selected.length < 4) {{
            if (!previousSet.has(q.question) || repeats >= 2) {{
              selected.push(q);
            }} else if (repeats < 2) {{
              selected.push(q);
              repeats++;
            }}
          }}
        }}
        while (selected.length < 4) {{
          for (let q of regionQuestions) {{
            if (!selected.includes(q)) {{
              selected.push(q);
              if (previousSet.has(q.question)) repeats++;
              if (selected.length === 4) break;
            }}
          }}
        }}
        newQuiz = newQuiz.concat(selected.slice(0, 4));
      }});
      if (repeats > 2) return selectQuiz();
      return newQuiz;
    }}

    function loadQuiz(quizQuestions) {{
      const form = document.getElementById('quizForm');
      form.innerHTML = '';
      quizQuestions.forEach((q, idx) => {{
        form.innerHTML += `<div class="question">
          <b>Q${{idx + 1}} (${{q.region}}):</b> ${{q.question}}<br>
          ${{q.options.map(opt =>
            `<label><input type="radio" name="q${{idx}}" value="${{opt}}"> ${{opt}}</label>`
          ).join(' ')}}
        </div>`;
      }});
    }}

    function submitQuiz() {{
      let score = 0;
      previousQuiz.forEach((q, idx) => {{
        const selected = document.querySelector(`input[name="q${{idx}}"]:checked`);
        if (selected && selected.value === q.answer) score++;
      }});
      document.getElementById('result').innerHTML =
        `<span>Your Score: ${{score}} / ${{previousQuiz.length}}</span>`;
    }}

    function resetQuiz() {{
      if (allQuestions.length === 0) return;
      const quizQuestions = selectQuiz();
      previousQuiz = quizQuestions;
      loadQuiz(quizQuestions);
      document.getElementById('result').innerHTML = '';
    }}
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print("Quiz HTML page generated as 'index.html'. Place both files in the same directory (or GitHub repo).")
