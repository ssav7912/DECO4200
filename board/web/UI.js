
CONSUMPTIONPLOT = null;


/*updates the time nodes with the current time*/
function updateTime(){
    time = document.getElementById("time");
    date = document.getElementById("date");
    current = new Date();
    time.textContent = current.toLocaleTimeString();
    date.textContent = current.toLocaleDateString();
}

/* 
Retrieves and renders appropriate utility usage data for the button pressed
*/
function graphbutton(buttonid) {
    console.log(buttonid);
    eel.getData(buttonid)(n => {UpdateconsumptionPlot(n[1], n[0])});    
}

/* 
Render code for updating utility plot
*/
function UpdateconsumptionPlot(datax, datay) {
    cons = document.getElementById("consume");

    trace = {'x': [datax], 'y': [datay], 'type': 'scatter'};
    cons.data[0].x = datax;
    cons.data[0].y = datay;
    Plotly.redraw(cons);
}


/* 
Generates utility usage plot
*/
eel.expose(newConsumptionPlot);
function newConsumptionPlot(datax, datay) {
    cons = document.getElementById("consume");
    const layout = { 
            width: 600,
            plot_bgcolor: "#666980",
            paper_bgcolor: "#666980",
            font: {color: "whitesmoke"},

        }
    
    CONSUMPTIONPLOT = Plotly.newPlot(cons, [{
        x: datax,
        y: datay,
        type: 'scatter',
        fill: 'tozeroy',
        mode: 'none',
        fillcolor:"#ffdd67",
        line: {
            color: "whitesmoke",
        }
    }], layout)
    // Plotly.update()
}


eel.expose(updateLights)
function updateLights(lightsOn) {
    lights = document.getElementById("Lights");
    lights.textContent = lightsOn;
}

/* 
Called on startup to generate containers for all the residents in the household
*/
eel.expose(generateResidents);
function generateResidents(residents) {
    container = document.getElementById("residentsContainer");

    for (const resident of residents) {
        res = JSON.parse(resident)
        container.appendChild(residenttemplate(res));

    }
}



eel.expose(updateResidentWrapper);
function updateResidentWrapper(residentjson) {
    const resident = JSON.parse(residentjson);
    updateResident(resident);
}

eel.expose(CreateResidentCardWrapper);
function CreateResidentCardWrapper(residentjson) {
    const resident = JSON.parse(residentjson);
    const clone = residenttemplate(resident);

    container = document.getElementById("residentsContainer");
    container.appendChild(clone);
}

function updateResident(resident) {
    console.log(resident)
    element = document.getElementById(resident.id);


    element.firstElementChild.querySelectorAll("text")[0].textContent = resident.emoji;
    element.firstElementChild.querySelectorAll("circle")[1].style.stroke = RESIDENTSTATUS[resident.status];

    // element.children[2].textContent = RESIDENTSTRINGMAP[resident.status];
    element.children[2].textContent = resident.statstring; 

}

eel.expose(createApplianceWrapper)
function createApplianceWrapper(appliancejson) {
    const appliance = JSON.parse(appliancejson);
    createAppliance(appliance);
}

function createAppliance(appliance) {
    const clone = appliancetemplate(appliance);
    container = document.getElementById("statuscontainer").appendChild(clone);
}

function appliancetemplate(appliance) {
   template = document.getElementById("ApplianceTemplate");

   const clone = template.content.cloneNode(true);

   clone.firstElementChild.children[1].textContent = appliance.name; 
   clone.firstElementChild.children[2].textContent = appliance.mode;
   clone.firstElementChild.children[0].firstElementChild.style.width = String(appliance.timeleft) + "%";

    return clone;
}


//main
updateTime();
window.setInterval(updateTime, 1000);

eel.getData("ELECTRICITY")(n => {newConsumptionPlot(n[1], n[0])});
// eel.getResidents()(n => {generateResidents(n)});
eel.getLights()(n => {updateLights(n)});
eel.getName()(n => {document.getElementById("groupname").textContent = n})
eel.getAppliances()(n => {
    for (const appliancejson of n) {
        // const appliance = JSON.parse(appliancejson);
        createAppliance(appliancejson);
    }
})