function smoothScrollTo(container, element, duration) {
  const startingY = container.scrollTop;
  const elementRect = element.getBoundingClientRect();
  const containerRect = container.getBoundingClientRect();

  // Calculate the element's top position relative to the container
  const elementTop = elementRect.top - containerRect.top + startingY;

  // Set the target to the element's top position
  const targetY = elementTop;
  const diff = targetY - startingY;
  let start;

  // Easing function: easeInOutCubic
  //https://gist.github.com/gre/1650294
  function easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
  }

  function step(timestamp) {
    if (!start) start = timestamp;
    const time = timestamp - start;
    let percent = Math.min(time / duration, 1);
    percent = easeInOutCubic(percent);

    container.scrollTop = startingY + diff * percent;

    if (time < duration) {
      window.requestAnimationFrame(step);
    }
  }

  window.requestAnimationFrame(step);
}

function parseId(id) {
  const idParts = id.split("_");
  return {
    x: parseInt(idParts[2]),
    y: parseInt(idParts[4]),
  };
}
function highlightInputs(input) {
  // check if input is div or input
  if (input.tagName === "DIV") {
    console.log("div");
    return false;
  } else {
    input.classList.add("highlight");
    return true;
  }
}

function highlightInputsArray(inputs) {
  //console.log(inputs);
  let wordDataNumberArray = [];
  inputs.forEach((input) => {
    highlightInputs(input);
    //get input word-data-number
    let wordDataNumber = input.getAttribute("word-data-number");
    //split data with ,
    for (let i = 0; i < wordDataNumber.split(",").length; i++) {
      wordDataNumberArray.push(wordDataNumber.split(",")[i]);
    }
    //console.log(wordDataNumberArray);
  });
  //find the most repeat elem in the array
  let numberDataDict = {};
  for (let i = 0; i < wordDataNumberArray.length; i++) {
    if (numberDataDict[wordDataNumberArray[i]] == null) {
      numberDataDict[wordDataNumberArray[i]] = 1;
    } else {
      numberDataDict[wordDataNumberArray[i]] += 1;
    }
  }
  // console.log(numberDataDict);

  //get the word-data-number with the most value
  let wordDataNumber;
  let maxVal = 0;

  for (let key in numberDataDict) {
    if (numberDataDict[key] > maxVal) {
      maxVal = numberDataDict[key];
      wordDataNumber = key;
    }
  }

  console.log(wordDataNumber);
  //highlight all clue with the word-data-number
  let clues = document.querySelectorAll('[id^="clue_"]');

  clues.forEach((clue) => {
    if (clue.getAttribute("id") === `clue_${wordDataNumber}`) {
      const container = document.querySelector(".cluestable");
      smoothScrollTo(container, clue, 500);
      //clue.classList.add('highlight');
      clue.classList.add("highlight_table_row");
    }
  });
}

let moveAlongX = true;
function inputsEvent() {
  const inputs = document.querySelectorAll('input[type="text"]');

  inputs.forEach((input) => {
    const { x, y } = parseId(input.id);
    //highlight inputs along x axis or y axis depending on which one is clicked
    input.addEventListener("focus", (e) => {
      //calculate the moveAlongX
      let prevXInput = document.getElementById(`input_X_${x - 1}_Y_${y}`);
      let nextXInput = document.getElementById(`input_X_${x + 1}_Y_${y}`);
      let prevYInput = document.getElementById(`input_X_${x}_Y_${y - 1}`);
      let nextYInput = document.getElementById(`input_X_${x}_Y_${y + 1}`);
      if (moveAlongX) {
        if (prevXInput == null && nextXInput == null) {
          moveAlongX = false;
        }
      } else {
        if (prevYInput == null && nextYInput == null) {
          moveAlongX = true;
        }
      }

      if (moveAlongX) {
        let inputArray = [];
        for (let i = x + 1; i < 20; i++) {
          const id = `input_X_${i}_Y_${y}`;
          const input = document.getElementById(id);
          if (input == null) {
            break;
          }
          inputArray.push(input);
          //highlightInputs(input);
        }
        for (let i = x - 1; i >= 0; i--) {
          const id = `input_X_${i}_Y_${y}`;
          const input = document.getElementById(id);
          if (input == null) {
            break;
          }
          inputArray.push(input);
          //highlightInputs(input);
        }
        highlightInputsArray(inputArray);
      } else {
        let inputArray = [];
        for (let i = y + 1; i < 20; i++) {
          const id = `input_X_${x}_Y_${i}`;
          const input = document.getElementById(id);
          if (input == null) {
            break;
          }
          inputArray.push(input);
          //highlightInputs(input);
        }
        for (let i = y - 1; i >= 0; i--) {
          const id = `input_X_${x}_Y_${i}`;
          const input = document.getElementById(id);
          if (input == null) {
            break;
          }
          inputArray.push(input);
          //highlightInputs(input);
        }
        highlightInputsArray(inputArray);
      }
    });

    //remove highlight from all inputs
    input.addEventListener("blur", () => {
      inputs.forEach((input) => {
        input.classList.remove("highlight");
      });
      //remove highlight from all clues (id starts with clue_)
      let clues = document.querySelectorAll('[id^="clue_"]');
      clues.forEach((clue) => {
        //clue.classList.remove('highlight');
        clue.classList.remove("highlight_table_row");
      });
    });

    function getNextInput(moveAlongX, currentInput) {
      const { x, y } = parseId(currentInput.id);
      let inputArray = [];
      if (moveAlongX) {
        for (let i = x + 1; i < 20; i++) {
          const id = `input_X_${i}_Y_${y}`;
          const input = document.getElementById(id);
          if (input == null) {
            break;
          }
          inputArray.push(input);
        }
      } else {
        for (let i = y + 1; i < 20; i++) {
          const id = `input_X_${x}_Y_${i}`;
          const input = document.getElementById(id);
          if (input == null) {
            break;
          }
          inputArray.push(input);
        }
      }
      console.log("moveX",moveAlongX,"\ngetNextInput", inputArray);
      if (inputArray.length === 0) {
        return null;
      }
      if (inputArray[0].tagName === "DIV") {
        //check until not DIV
        for (let i = 0; i < inputArray.length; i++) {
          if (inputArray[i].tagName !== "DIV") {
            return inputArray[i];
          }
        }
      } else {
        return inputArray[0];
      }
    }

    function getPreviousInput(moveAlongX, currentInput) {
      const { x, y } = parseId(currentInput.id);
      let inputArray = [];
      if (moveAlongX) {
        for (let i = x - 1; i >= 0; i--) {
          const id = `input_X_${i}_Y_${y}`;
          const input = document.getElementById(id);
          if (input == null) {
            break;
          }
          inputArray.push(input);
        }
      } else {
        for (let i = y - 1; i >= 0; i--) {
          const id = `input_X_${x}_Y_${i}`;
          const input = document.getElementById(id);
          if (input == null) {
            break;
          }
          inputArray.push(input);
        }
      }
      //reverse the array
      inputArray.reverse();
      if (inputArray.length === 0) {
        return null;
      }
      for (let i = inputArray.length - 1; i >= 0; i--) {
        if (inputArray[i].tagName !== "DIV") {
          return inputArray[i];
        }
      }
    }

    //move to next input when a letter is entered
    input.addEventListener("input", (e) => {
        console.log(e.inputType);
      if (e.inputType === "deleteContentBackward") {
        return;
      }
      getNextInput(moveAlongX, e.target).focus();
    });

    input.addEventListener("keydown", (e) => {
      //backspace event
      if (e.key === "Backspace") {
        if (input.value !== "") {
          return;
        }
        getPreviousInput(moveAlongX, input).focus();
      }
      //arrow event
      else if (e.key === "ArrowRight") {
        moveAlongX = true;
        let nextInput = getNextInput(moveAlongX, input);
        nextInput.focus();
      } else if (e.key === "ArrowLeft") {
        moveAlongX = true;
        let prevInput = getPreviousInput(moveAlongX, input);
        prevInput.focus();
      } else if (e.key === "ArrowUp") {
        moveAlongX = false;
        let prevInput = getPreviousInput(moveAlongX, input);
        //sleep 0.1s
        prevInput.focus();
      } else if (e.key === "ArrowDown") {
        moveAlongX = false;
        let nextInput = getNextInput(moveAlongX, input);
        nextInput.focus();
      }
    });
  });
}

function clickClue() {
  const clues = document.querySelectorAll('[id^="clue_"]');
  clues.forEach((clue) => {
    clue.addEventListener("click", () => {
      //focus first available input
      //get clue number
      const clueNumber = clue.getAttribute("id").split("_")[1];
      //get all inputs with the same word-data-number
      //word-data-number="H1,V3"

      const inputs = document.querySelectorAll(
        `[word-data-number*="${clueNumber}"]`
      );
      //get across or down
      let moveAlongXforClue =
        clue.children[1].innerText === "across" ? true : false;
      //set global moveAlongX
      moveAlongX = moveAlongXforClue;
      //focus on the first input that not div
      console.log("===================================");
      for (let i = 0; i < inputs.length; i++) {
        console.log("click to focus", inputs[i].id);
        if (inputs[i].tagName !== "DIV") {
          inputs[i].focus();
          break;
        }
      }
    });
  });
}

document.body.addEventListener("htmx:afterSwap", function (event) {
  let moveAlongX = true;
  inputsEvent();
  clickClue();
  //input button name show_hint
});

//check if page is reload or be redirected
let performanceEntries = performance.getEntriesByType("navigation");

if (performanceEntries.length > 0) {
  let navigationEntry = performanceEntries[0];
  if (
    navigationEntry.type === "navigate" ||
    navigationEntry.type === "reload"
  ) {
    //after page load success
    document.addEventListener("DOMContentLoaded", function () {
      //sleep 0.1s

      setTimeout(function () {
        if (document.getElementsByName("check_crossword")[0] != null) {
          document.getElementsByName("check_crossword")[0].click();
        }
      }, 100);
    });
  }
}

// test repeat number of clue
const clues = document.querySelectorAll('[id^="clue_"]');

//if clue have same id highlight
let bool_repeat = false;
for (let i = 0; i < clues.length; i++) {
  for (let j = i + 1; j < clues.length; j++) {
    if (clues[i].getAttribute("id") === clues[j].getAttribute("id")) {
      clues[i].classList.add("highlight-red");
      clues[j].classList.add("highlight-red");
      bool_repeat = true;
    }
  }
}

if (!bool_repeat) {
  console.log("click reset");
}
