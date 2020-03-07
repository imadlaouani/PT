function timer(){
    const start = Date.now();

    var t;


     var fin = start + 7200000;
     timedCount();




    function timedCount() {
      var ptmp = new Date();
      var tempRest = fin - ptmp
      var diff = new Date(tempRest)
      diff.setHours(diff.getHours() - 1)
      var d = diff.toLocaleTimeString();
      if (tempRest > 0){
        document.getElementById("demo").innerHTML = d;

      }
      else {
        document.getElementById("demo").innerHTML = "Terminé !!";
        document.location.href="http://127.0.0.1:8000/corriger/{{sub.numSujet}}";


      }


      t = setTimeout(timedCount, 1);




    }
}