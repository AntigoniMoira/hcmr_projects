class AjaxError {
    constructor(error) {
        this.status = error.status;
        //this.name = error.name;

        if (error.statusText >= 200 && error.statusText <= 206) {
            this.msg = 'Επιτυχής καταχώρηση';
        } else if (error.statusText === 400) {
            this.msg = 'Παρακαλούμε ελέγξτε ξανά τα εισαχθέντα στοιχεία';
        } else if (error.statusText === 401) {
            this.msg = 'Unauthorized';
        } else if (error.statusText === 404) {
            this.msg = 'Η σελίδα αυτή δεν είναι διαθέσιμη';
        } else if (error.statusText >= 500 && error.statusText <= 511) {
            this.msg = 'Παρουσιάστηκε πρόβλημα στον server';
        } 
        else {
            this.msg = 'Κάτι πήγε στραβά. Παρακαλούμε προσπαθήστε ξανά σε λίγο.';
        }

    }

    //methods here
    printError() {
        console.error(this);
    }

} // end of class

export default AjaxError