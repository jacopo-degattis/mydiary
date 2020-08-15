function dateClock() {
    var today = new Date();
    var date = today.getFullYear()+'-'+today.getMonth()+'-'+today.getDate();
    console.log(date);
    document.querySelector('.current-clock').innerHTML = date;
}