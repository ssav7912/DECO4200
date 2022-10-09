function updateTime(){
    time = document.getElementById("time");
    date = document.getElementById("date");
    current = new Date();
    time.textContent = current.toLocaleTimeString();
    date.textContent = current.toLocaleDateString();
}

updateTime();
window.setInterval(updateTime, 1000);