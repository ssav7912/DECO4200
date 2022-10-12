class Person {
    name;
    id;
    status;
    
    constructor(name, id) {
      this.name = name;
      this.id = name;
    }


    newStatus(status) {
      this.status = status;
    }

    toJSON() {

      return '{ "name":"' + this.name + '", "id":"' + this.id + '", "location: HOME", "status": "' + this.status + '"}'; 
    }
  }