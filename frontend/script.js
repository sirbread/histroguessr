let correctYear = null;

async function loadArticle() {
  const res = await fetch("http://localhost:8000/event");
  const data = await res.json();

  document.getElementById("article-container").innerHTML = data.html;
  correctYear = data.answer;

  console.log("correct year:", correctYear);

  document.getElementById("result").textContent = "";
  document.getElementById("year").value = "";
  document.getElementById("next").style.display = "none";
}

function scoreGuess(guess, actual) {
  const diff = Math.abs(guess - actual);
  if (diff === 0) return 100;
  if (diff <= 2) return 90;
  if (diff <= 5) return 75;
  if (diff <= 10) return 60;
  if (diff <= 25) return 40;
  if (diff <= 50) return 20;
  return 0;
}

document.getElementById("submit").onclick = () => {
  const guess = parseInt(document.getElementById("year").value);
  console.log("guess:", guess, "correct year:", correctYear);

  if (isNaN(guess) || correctYear === null) {
    console.warn("shit got cooked");
    return;
  }

  const score = scoreGuess(guess, correctYear);
  document.getElementById("result").textContent =
    `you guessed ${guess}. the correct year was ${correctYear}. score: ${score}/100`;
  document.getElementById("next").style.display = "inline-block";
};

document.getElementById("next").onclick = loadArticle;

loadArticle();
