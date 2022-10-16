


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

housemates = [new Person("Soren", "Soren"), new Person("Trang", "Trang"), new Person("Sajitha", "Sajitha"), new Person("David", "David")];
renderHouseMates(housemates);