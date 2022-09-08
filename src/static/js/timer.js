let idleTime = 0;
document.addEventListener('DOMContentLoaded', () => {

    setInterval(timerIncrement, 1000); // 1 sec

    //Zero the idle timer on mouse movement.
    document.addEventListener('mousemove', function () {
        idleTime = 0;
    });
    document.addEventListener("keypress", function () {
        idleTime = 0;
    });
});

function timerIncrement() {
    idleTime = idleTime + 1;

    if (idleTime > 60) { // 60 sec
        let xhr = new XMLHttpRequest();
        xhr.open('GET', "/");
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");


        xhr.send(JSON.stringify({
            "disable_server": true,
        }));

        xhr.onload = function () {

            window.location.reload();
        }

        idleTime = 0;
    }
}
