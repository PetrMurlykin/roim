// Get a reference to the view container
const viewContainer = document.getElementById('viewContainer');

let examplesData;

async function fetchExamples() {
    try {
        const response = await fetch('/api/examples');
        const data = await response.json();
        examplesData = data;
    } catch (error) {
        console.error(error);
    }
}

function populateExamples() {
    for(let ex = 0; ex < examplesData['examples'].length; ex++) {
        const container = document.createElement('div');
        container.id = `container${ex}`;
        container.classList.add('container');

        let example = examplesData['examples'][ex];
        const newView = document.createElement('p');
        newView.textContent = '{a} {operator} {b} = '
        .replace('{a}', example['a'])
        .replace('{operator}', example['operator'])
        .replace('{b}', example['b']);
        container.appendChild(newView);

        let canvas = addCanvas(ex);
        container.appendChild(canvas);

        const button = createButton('Check', function() {
            handleCheckClick(ex)
        })
        container.appendChild(button);

        const result = document.createElement('p');
        result.id = `result${ex}`;
        container.appendChild(result);

        viewContainer.appendChild(container);
    }
}

function handleCheckClick(index) {
    let example = examplesData['examples'][index];
    var formdata = new FormData();

    const canvas = document.getElementById(`canvas${index}`);
    const answerP = document.getElementById(`result${index}`);

    canvas.toBlob(function (blob) {
        formdata.append('image', blob, 'image.png');
        formdata.append('data', JSON.stringify(example));

        var requestOptions = {
            method: 'POST',
            body: formdata,
            redirect: 'follow'
          };
    
        fetch('api/answer', requestOptions)
          .then(response => response.json())
          .then(data => {
              console.log(data);
              if(data['isCorrect']){
                answerP.textContent = 'OK';
              } else {
                answerP.textContent = 'Wrong. Predicted is ' + data['prediction'];
              }
          })
          .catch(error => {
            console.log(error);
          });
      }, 'image/png');
}

function addCanvas(index) {
    
    const canvasId = `canvas${index}`;
  
    const canvas = document.createElement('canvas');
    canvas.id = canvasId;
    canvas.width = 112;
    canvas.height = 56;
  
    // Enable drawing on the canvas
    enableDrawing(canvas);

    return canvas;
  }
  
  function enableDrawing(canvas) {
    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;
    
    const ctx = canvas.getContext('2d');
    ctx.lineWidth = 4;
  
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);
  
    function startDrawing(e) {
      isDrawing = true;
      [lastX, lastY] = [e.offsetX, e.offsetY];
    }
  
    function draw(e) {
      if (!isDrawing) return;
      ctx.beginPath();
      ctx.moveTo(lastX, lastY);
      ctx.lineTo(e.offsetX, e.offsetY);
      ctx.stroke();
      [lastX, lastY] = [e.offsetX, e.offsetY];
    }
  
    function stopDrawing() {
      isDrawing = false;
    }
}

function createButton(text, onClickHandler) {
    const button = document.createElement('button');
    button.textContent = text;
    button.addEventListener('click', onClickHandler);
    return button;
}

async function main() {
    await fetchExamples();
    console.log(examplesData);
    populateExamples();
}

main();

