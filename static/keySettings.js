/**
 * Created by Nicola Malloy on 11/18/2016.
 */

//declare global variables for the key presses
////initialized to the bottom row of keyboard

var key_map ={
    "a":65,
    "b":66,
    "c":67,
    "d":68,
    "e":69,
    "f":70,
    "g":71,
    "h":72,
    "i":73,
    "j":74,
    "k":75,
    "l":76,
    "m":77,
    "n":78,
    "o":79,
    "p":80,
    "q":81,
    "r":82,
    "s":83,
    "t":84,
    "u":85,
    "v":86,
    "w":87,
    "x":88,
    "y":89,
    "z":90,
    "space":32
};

    ckey = "z";
    cskey = "s"; //s
    dkey = "x"; //x
    dskey = "d"; //d
    ekey = "c"; //c
    fkey = "v"; //v
    fskey = "g"; //g
    gkey = "b"; //b
    gskey = "h"; //h
    akey = "n"; //n
    askey = "j"; //j
    bkey = "m"; //m

    loadDefault = 0;


function NoteChange(noteVal, keyVal) {
       console.log("here ugh");
       //Function to change the key press for the corresponding note
       if(noteVal == "ckey"){
           ckey = keyVal;
           document.getElementById("c").innerHTML = ckey;
       }
       else if(noteVal == "cskey"){
           cskey = keyVal;
           document.getElementById("cs").innerHTML = cskey;
       }
       else if(noteVal == "dkey"){
           dkey = keyVal;
           document.getElementById("d").innerHTML = dkey;
       }
       else if(noteVal == "dskey"){
           dskey = keyVal;
           document.getElementById("ds").innerHTML = dskey;
       }
       else if(noteVal == "ekey"){
           ekey = keyVal;
           document.getElementById("e").innerHTML = ekey;
       }
       else if(noteVal == "fkey"){
           fkey = keyVal;
           document.getElementById("f").innerHTML = fkey;
       }
       else if(noteVal == "fskey"){
           fskey = keyVal;
           document.getElementById("fs").innerHTML = fskey;
       }
       else if(noteVal == "gkey"){
           gkey = keyVal;
           document.getElementById("g").innerHTML = gkey;
       }
       else if(noteVal == "gskey"){
           gskey = keyVal;
           document.getElementById("gs").innerHTML = gskey;
       }
       else if(noteVal == "akey"){
           akey = keyVal;
           document.getElementById("a").innerHTML = akey;
       }
       else if(noteVal == "askey"){
           askey = keyVal;
           document.getElementById("as").innerHTML = askey;
       }
       else if(noteVal == "bkey"){
           bkey = keyVal;
           document.getElementById("b").innerHTML = bkey;
       }

       loadDefault = 1;
       console.log(ckey);
       console.log(loadDefault);
   }