var xValues = ["on Time", "Risky", "Terminated", "Late","cancel"];
var yValues = [ 15, 16, 10, 14, 5];
var click = true;
var barColors = [
    "rgba(30,132,127,1.0)",
    "rgba(255,192,59,1.0)",
    "rgba(196,196,196,1.0)",
    "rgba(255,110,64,1.0)",
    "rgba(30,61,89,1.0)",
];

new Chart("myChart", {
    type: "pie",
    data: {
        labels: xValues,
        datasets: [{
            backgroundColor: barColors,
            data: yValues
        }]
    },
    options: {
        title: {
            display: true,
            text: "Dashboard",
            fontSize: 40,
            fontColor: '#105378',
        },
        legend: {
            position: 'left',
        },
    },
});

function clickIcon(){
    if(click){
        $('.carrosell').find('i').css('transform','rotate(-90deg)');
        click = false;
    }else{
        $('.carrosell').find('i').css('transform','rotate(90deg)');
        click = true;
    }
    
}
