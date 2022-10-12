
CONSUMPTIONPLOT = null;

function updateTime(){
    time = document.getElementById("time");
    date = document.getElementById("date");
    current = new Date();
    time.textContent = current.toLocaleTimeString();
    date.textContent = current.toLocaleDateString();
}

function graphbutton(buttonid) {
    console.log(buttonid);
    eel.getData(buttonid)(n => {UpdateconsumptionPlot(n[1], n[0])});    
}

function UpdateconsumptionPlot(datax, datay) {
    cons = document.getElementById("consume");

    trace = {'x': [datax], 'y': [datay], 'type': 'scatter'};
    cons.data[0].x = datax;
    cons.data[0].y = datay;
    Plotly.redraw(cons);
}

eel.expose(newConsumptionPlot);
function newConsumptionPlot(datax, datay) {
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

eel.expose(generateResidents);
function generateResidents(residents) {
    container = document.getElementById("residentsContainer");

    for (const resident of residents) {
        res = JSON.parse(resident)
        container.appendChild(residenttemplate(res.id));

    }
}

function residenttemplate(id) { 
    div = document.createElement("div");
    text = document.createElement("p");
    content = document.createTextNode(id);

    div.appendChild(text)
    text.appendChild(content)

    return div

}



//main
updateTime();
window.setInterval(updateTime, 1000);

eel.getData("ELECTRICITY")(n => {newConsumptionPlot(n[1], n[0])});
eel.getResidents()(n => {generateResidents(n)});
eel.getLights()(n => {updateLights(n)});