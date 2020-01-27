var audio = (function () {
    ////private variable
 var dict;

  
    return {
        set: function (data) {
            var dict=data;
           

        },
         datas: function () {

               return dict;
        }

    };
})();

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




  
  //////initialize data table
    var table = $('#audio-table').DataTable({
        destroy: true,
        paging:   false,
        ordering: true,
        info:     false,
        searching: true,
    

        columns: [
            { data: null, render: 'id',visible: false },
            { data: null, render: 'url',visible: false },
            { data: null, render: 'name', className: "align-middle" },
            { data: null, render: 'language', className: "align-middle" },
            { data: null, render: 'voice_type', className: "align-middle" },

            { data: null, render: 'voice_name', className: "align-middle" },
            { data: null, render: 'device_profile', className: "align-middle" },
            { data: null, render: 'speed', className: "align-middle" },
            { data: null, render: 'pitch', className: "align-middle" },



             { data: null,"render": function ( data, type, row, meta ) {
                    
                    var play_pause='<a id="play-pause-button" class="fa fa-play" style="margin-left:4px"></a>';
                    var edit='<a id="edit-button" class="fa fa-pencil-square-o" style="margin-left:4px"></a>';
                    var download='<a id="download-button" class="fa fa-cloud-download" style="margin-left:4px"></a>';
                    var del='<a id="del-button" class="fa fa-trash" style="margin-left:8px;margin-right:4px"></a>';
                    return  play_pause+edit+download+del;
                     }
              },

           
        ],
    
    });




    

    //$('#audio-table tbody').on( 'click', 'a', function (){
      //if( $(this).attr('id')=="play-pause-button") {      
       // if($(this).hasClass('fa-play')){
         
         //$(this).removeClass('fa-play');
         //$(this).addClass('fa-pause');

         //var data = table.row( $(this).parents('tr') ).data();
         //audio.datas()[data[0]].play();
         //audio.datas(data[0]).onended = function() {
           // $("#play-pause-button").removeClass('fa-pause');
            //$("#play-pause-button").addClass('fa-play');
            //};

         
       //  }

   
        
      //  else{
        // $(this).removeClass('fa-pause');
         //$(this).addClass('fa-play');
         //audio.datas(data[0]).pause();
        //}


      //}
      //});







   var tdf=$("#table-data-form");
   $.ajax({
            url: tdf.attr("js-table-data-url"),
            type: tdf.attr("method"),
            data: tdf.serialize(),
            credentials: 'include',

           
            success: function (data, textStatus, xhr) {

                  
              // data.redirect contains the string URL to redirect to
                  
               
               
               $('.fa-spinner').css("display","none");
               //var a = JSON.parse(data);
              // $('#a-output').attr('href',data.audio_url);
               //$('#a-output').html(data.audio_url);
                //$('.fa-check').css("display","inline");
               var data = JSON.parse(data);
               table.clear();
               var temp=[];
               for(i=0;i<data.length;i++){
                   table.row.add(data[i]);
                   //temp[i]=new Audio(data[i].url);
                   


               }
               table.draw();
               // audio.set(temp);
                



            },


            error: function (request, status, error) {
                 $('.fa-spin').css("display","none");
                 
                 //$('.fa-close').css("display","inline");
                  alert('error');
                 
                
            },
         
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
            credentials: 'include',

           
            success: function (data, textStatus, xhr) {

                  
              // data.redirect contains the string URL to redirect to
                  
               
               
               $('.fa-spinner').css("display","none");
               //var a = JSON.parse(data);
               $('#a-output').attr('href',data.audio_url);
               $('#a-output').html(data.audio_url);
                //$('.fa-check').css("display","inline");
                
                



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
