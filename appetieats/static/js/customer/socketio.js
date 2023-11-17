const socket = io.connect('http://' + document.domain + ':' + location.port + '/customer');

socket.on("connect", function() {
    console.log("Connected into socketio");
});

socket.on("update_customer_view", function() {
    init();
    const bell = new Audio('/static/assets/mp3/bell.mp3');
    bell.play();
});

