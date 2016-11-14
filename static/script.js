/**
 * Created by alefevre on 10/18/16.
 */
function playNote(evt) {
    var  key_press = "C-3";
    alert(0); 
    $.ajax({
        url: '/PianoPlayer.py',
        data: {note: key_press},
        type: 'POST',
        success: function (response) {
            console.log(response);
        },
        error: function (error) {
            console.log(error);
        }
    });
}