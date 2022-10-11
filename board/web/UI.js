
CONSUMPTIONPLOT = null;

function updateTime(){
    time = document.getElementById("time");
    date = document.getElementById("date");
    current = new Date();
    time.textContent = current.toLocaleTimeString();
    date.textContent = current.toLocaleDateString();
}

function UpdateconsumptionPlot(buttonID) {
    cons = document.getElementById("consume");

}

eel.expose(newConsumptionPlot);
function newConsumptionPlot(datax, datay) {
    console.log("hit");
    console.log(datax, datay)
    cons = document.getElementById("consume")
    CONSUMPTIONPLOT = Plotly.newPlot(cons, [{
        x: datax,
        y: datay,
        type: 'scatter'
    }])
    Plotly.update()
}

eel.expose(updateLights)
function updateLights(lightsOn) {
    lights = document.getElementById("Lights");
    lights.textContent = lightsOn;
}


//main
updateTime();
window.setInterval(updateTime, 1000);
