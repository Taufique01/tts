
var globaloptions = {
    en_AU: [
        "en-AU-Standard-A",
        "en-AU-Standard-B",
        "en-AU-Standard-C",
        "en-AU-Standard-D", 
        "en-AU-Wavenet-A", 
        "en-AU-Wavenet-B", 
        "en-AU-Wavenet-C",
        "en-AU-Wavenet-D",
    ],
    en_IN: [
        "en-IN-Standard-A",
        "en-IN-Standard-B",
        "en-IN-Standard-C",
         "en-IN-Wavenet-A",
         "en-IN-Wavenet-B",
         "en-IN-Wavenet-C", 
    ],

    en_GB: [
        "en-GB-Standard-A",
        "en-GB-Standard-B",
        "en-GB-Standard-C",
        "en-GB-Standard-D", 
        "en-GB-Wavenet-A", 
        "en-GB-Wavenet-B", 
        "en-GB-Wavenet-C",
        "en-GB-Wavenet-D",
    ],
    en_US: [
        "en-US-Standard-A",
        "en-US-Standard-B",
        "en-US-Standard-C",
        "en-US-Standard-D",
        "en-US-Standard-E", 
        "en-US-Wavenet-A", 
        "en-US-Wavenet-B", 
        "en-US-Wavenet-C",
        "en-US-Wavenet-D",
        "en-US-Standard-E", 
        "en-US-Wavenet-F", 
       
    ],
     
    
};

$(document).ready(function (event) {

    $("#language").change(function(){
        var selectedClass = $(this).find("option:selected").attr("class");    
        var options = globaloptions[selectedClass];
        var newoptions = "";
        for(var i = 0; i < options.length; i++){
            newoptions+='<option value="'+options[i]+'"' +' >'+ options[i] +'</option>';                            
        }
        $("#voice-name").html(newoptions);
    });  

    $("#range-speed").change(function(){
       $("#speed-val").html(""+ $(this).val()/100);
    });  




   $("#range-pitch").change(function(){
       $("#pitch-val").html(""+ $(this).val()/10);
    });  






    $("#tts-form").submit(function (event) {

        event.preventDefault();
       $('.fa-spinner').css("display","inline");       
        //$('.fa-check').css("display","none");
        //$('.fa-close').css("display","none");
 

        var formData = new FormData(this);
         $.ajax({
            url: $(this).attr("js-tts-url"),
            type: $(this).attr("method"),
            data: formData,
           
            success: function (data) {
               $('.fa-spinner').css("display","none");
               //var a = JSON.parse(data);
               $('#a-output').attr('href',data.audio_url);
               $('#a-output').html(data.audio_url);
                //$('.fa-check').css("display","inline");
                
                
                //$('#z-total').html(Zillow.datas().length);
                //updateZillowView();

             alert('success');
            },


            error: function (request, status, error) {
                 $('.fa-spin').css("display","none");
                 
                 //$('.fa-close').css("display","inline");
                  alert('error');
                 
                
            },
            cache: false,
            contentType: false,
            processData: false
        });


    });
});
