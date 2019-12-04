// 描画
window.addEventListener('load', () => {
  const canvas = document.querySelector('#draw-area');
  const context = canvas.getContext('2d');
  const lastPosition = { x: null, y: null };
  let isDrag = false;

  function draw(x, y) {
    if(!isDrag) {
      return;
    }

    context.lineCap = 'round';
    context.lineJoin = 'round';
    context.lineWidth = 20; // 線の太さ
    context.strokeStyle = 'black'; // 線の色

    if (lastPosition.x === null || lastPosition.y === null) {
      // ドラッグ開始時の線の開始位置
      context.moveTo(x, y);
    } else {
      // ドラッグ中の線の開始位置
      context.moveTo(lastPosition.x, lastPosition.y);
    }

    context.lineTo(x, y);

    context.stroke();

    lastPosition.x = x;
    lastPosition.y = y;
  }

  function clear() {
    context.fillStyle = "rgb(255,255,255)";
    context.fillRect(0, 0, canvas.getBoundingClientRect().width, canvas.getBoundingClientRect().height);
  }

  function dragStart(event) {
    context.beginPath();
    isDrag = true;
  }

  function dragEnd(event) {
    context.closePath();
    isDrag = false;

    lastPosition.x = null;
    lastPosition.y = null;
  }

  function send() {
    var img = document.getElementById("draw-area").toDataURL('image/png');
    img = img.replace('image/png', 'image/octet-stream');
    $.ajax({
        type: "POST",
        url: "http://localhost:5000",
        data: {
            "img": img
        }
    })
    .done( (data) => {
        $('#answer').html(data['ans'] + "(" + data['per'] + "%)");
        $("#saveImg").attr("src", "/static/images/pure/" + data['now_time'] + ".jpg");
        $("#inverseImg").attr("src", "/static/images/inverse/" + data['now_time'] + ".jpg");
        clear();
    });
  }

  function initEventHandler() {
    const clearButton = document.querySelector('#clear-button');
    clearButton.addEventListener('click', clear);

    const sendButton = document.querySelector('#img');
    sendButton.addEventListener('click', send);

    canvas.addEventListener('mousedown', dragStart);
    canvas.addEventListener('mouseup', dragEnd);
    canvas.addEventListener('mouseout', dragEnd);
    canvas.addEventListener('mousemove', (event) => {
      draw(event.layerX, event.layerY);
    });

    clear();
  }

  initEventHandler();

});
