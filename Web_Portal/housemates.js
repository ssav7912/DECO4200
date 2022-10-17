


function renderHouseMates(housemateslist) {
    container = document.getElementById("Housematesgrid");
    for (const housemate of housemateslist) {
        node = residenttemplate(housemate);
        container.appendChild(node);
    }
}


function generateHousemateCard(name, status, photo) {

    div = document.createElement("div");
    p = document.createElement("name");
    p2 = document.createElement("status");

    nametext = document.createTextNode(name);
    statustext = document.createTextNode(status);

    p.appendChild(nametext);
    p2.appendChild(statustext);

    div.appendChild(p);
    div.appendChild(p2);

    return div;
}

async function getHousemates(housemateslist) {
    const url = window.location.href + "?users=true"
    const options = {method: "GET"};
    r = new Request(url, options);
    list = [...housemateslist];
    val = await fetch(r).then(response =>response.json());


    for (const str of val) {
        const obj = JSON.parse(str)
        resident = getResidentById(obj.id, housemateslist);
        if (resident == null) {
            
            newres = new Person(obj.name, obj.id);
            newres.status = obj.status;
            newres.emoji = obj.emoji;

          await list.push(newres)

        }
        else {
            resident.status = obj.status;
            resident.emoji = obj.emoji;
        }
    }    
    return list;
}

function getResidentById(id, residentlist) {
    for (const resident of residentlist) {
        if (resident.id == id) {
            return resident;
        }
    }

    return null;
}

// housemates = [new Person("Soren", "Soren"), new Person("Trang", "Trang"), new Person("Sajitha", "Sajitha"), new Person("David", "David")];
housemates = []
getHousemates(housemates).then(n => {renderHouseMates(n)});
