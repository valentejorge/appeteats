const socket = io.connect('http://' + document.domain + ':' + location.port + '/dashboard');

socket.on("connect", function() {
    console.log("Connected into socketio");
});

socket.on("new_order", function(order_data) {
    console.log(order_data);
    const page = document.querySelector(`#${order_data[0].status}`)
    const card = cardConstructor(order_data[0]);
    const bell = new Audio('/static/assets/mp3/bell.mp3');
    bell.play();
    page.insertAdjacentHTML("afterbegin", card);
});
