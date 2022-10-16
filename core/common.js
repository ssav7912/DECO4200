
//ugh i wish i had preprocesser symbols
RESIDENTSTATUS = {"AVAILABLE": "var(--available)", "BUSY": "var(--busy)", "AWAY": "var(--away)", "DONOTDISTURB": "var(--donotdisturb)"};



class Person {
  name;
  id;
  status;
  emoji;

  constructor(name, id) {
    this.name = name;
    this.id = name;
    this.status = "AVAILABLE";
    this.emoji = "😊";
  }


  newStatus(status) {
    this.status = status;
  }

  toJSON() {

    return '{ "name":"' + this.name + '", "id":"' + this.id + '", "location": "HOME", "status": "' + this.status + '", "emoji": "' + this.emoji + '"}';
  }
}

/* 
Generate resident container from template and resident object
*/
function residenttemplate(resident) { 
  template = document.getElementById("residentTemplate");


  const clone = template.content.cloneNode(true);
  clone.firstElementChild.id = resident.id;


  clone.firstElementChild.children[0].querySelectorAll("text")[0].textContent = resident.emoji;
  clone.firstElementChild.children[1].appendChild(document.createTextNode(resident.name));
  clone.firstElementChild.children[2].appendChild(document.createTextNode(resident.status));

  return clone

}