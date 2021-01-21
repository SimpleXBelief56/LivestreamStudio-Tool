var progressBar = document.querySelector('.w-0');
var progressBarText = document.querySelector('.progress-val-text');
var progressBarStatus = document.querySelector('.progress-status');
var resultCard = document.getElementById("resultSection");
var copy = undefined;
var PreserveValue = 0;
var AJAXRequestValue = [];
var AJAXComplete = false;
var percentage = 0;


// Predefined Values
var book = undefined;
var chapter = undefined;
var verse1 = undefined;
var verse2 = undefined;

function Delay(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}

function CopyToClipboard(str_buffer){
    var spwnText = document.createElement("textarea");
    spwnText.value = str_buffer;
    document.body.appendChild(spwnText);
    spwnText.select();
    document.execCommand("Copy");
    spwnText.remove();
    // var range = document.createRange();
    // range.selectNode(str_buffer);
    // window.setSelection().removeAllRanges();
    // window.setSelection().addRanges(range);
    // document.execCommand("copy");
    // window.getSelection().removeAllRanges();
    // console.log("Data has been copied to the clipboard");
}

async function writeData(book_param, chapter_param, first_verse_param, second_verse_param){
    $(document).ready(async function(){
        $(".progress-row").addClass("animate__animated animate__fadeOut").promise().done(async function(){
            await Delay(900);
            $(".progress-row").addClass("hide-out");
            await Delay(900);
            $("#resultSection").removeClass("hide-out");
        })
        $(".parse-body").css("height", "unset")
        $(".parse-body").removeClass("no-overflow");
        
    }).promise().done(function(){
        for(var i = 0; i < AJAXRequestValue.length; i++){
    
            const htmlOutput = `
            
            <div class="col-lg-12 mb-5">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${book_param} ${chapter_param}:${first_verse_param}-${second_verse_param}</h5>
                        <p id="parsedData" class="card-text">${AJAXRequestValue[i]}</p>
                        <a href="#" class="btn btn-primary copy-button">Copy</a>
                    </div>
                </div>
            </div>
            
            
            `
    
            resultCard.innerHTML += htmlOutput;
        }
        copy = $(".copy-button").click(function(e){
            console.log(e);
            console.log(e.target.parentElement.childNodes[3].innerText);
            CopyToClipboard(e.target.parentElement.childNodes[3].innerText);
        })
    })
}



function requestParsedVersesJSON(book, chapter, verse1, verse2, language){
    var parsedVersesArray = [];
    $.ajax({
        url: "/parse_data",
        type: "GET",
        dataType: "json",
        data: {book_field: book, chapter_field: chapter, verse1_field: verse1, verse2_field: verse2, language_field: language},
        success: function(requestedData){
            AJAXRequestValue = requestedData;
            for(var i = 0; i < requestedData.length; i++){
                AJAXRequestValue[i] = requestedData[i];

                // Out Of Memory Error (Potential Buffer Overflow)
                // AJAXRequestValue.push(requestedData[i]);
            }
            writeData(book, chapter, verse1, verse2);
            return requestedData
        }
    })
    return AJAXRequestValue;
}

function getPercentage(){
    var xhor = $.ajax({
        url: "/getPercentage",
        type: "GET",
        dataType: "json",
        success: function(val){
            PreserveValue = val[0];
            progressBar.style.width = PreserveValue + "%";
            progressBarText.innerHTML = PreserveValue + "%";
            progressBarStatus.innerHTML = val[1];
            if(PreserveValue !== val[0]){
                PreserveValue = val[0];
                console.log("success returned: "+ PreserveValue);
            }
            if(PreserveValue == "100"){
                progressBar.style.width = "100%";
                progressBarText.innerHTML = "100%";
                progressBarStatus.innerHTML = "Status: Completed"

                AJAXComplete = true;
            }
            return val;
            
        }
    });
    if(AJAXComplete){
        xhor.abort();
    }
}


$(document).ready(function(){
    $(".btn-parse-submit").click(async function(){
        var book = document.getElementById('book').value;
        var chapter = document.getElementById('chapter').value;
        var verse1 = document.getElementById('verse1').value;
        var verse2 = document.getElementById('verse2').value;
        var language = document.getElementById('language').value;
        $('.form-row-handler').addClass("animate__animated animate__fadeOut")
        await Delay(400);
        $('.form-row-handler').addClass("hide-out")
        await Delay(700);
        $('.progress-row').removeClass("hide-out")
        $('.progress-row').addClass("animate__animated animate__fadeInUp")
        await Delay(400);
        var requestedInformation = requestParsedVersesJSON(book, chapter, verse1, verse2, language);
        console.log("Function Return: " + requestedInformation);
        var percentage = setInterval(function(){
            $.ajax({
                url: "/getPercentage",
                type: "GET",
                dataType: "json",
                success: async function(val){
                    progressBar.style.width = PreserveValue + "%";
                    progressBarText.innerHTML = PreserveValue + "%";
                    progressBarStatus.innerHTML = val[1];
                    if(PreserveValue !== val[0]){
                        PreserveValue = val[0];
                        console.log("success returned: "+ PreserveValue + " " + val[2]);
                    }
                    if(val[2] == "Done"){
                        progressBar.style.width = "100%";
                        progressBarText.innerHTML = "100%";
                        progressBarStatus.innerHTML = "Status: Completed"
        
                        AJAXComplete = true;
                        if(AJAXComplete){
                            console.log("CLEAROUT INTERVAL");
                            clearInterval(percentage);
                        }
                    }
                    if(val[1] == "404"){
                        alert("Error has occured");
                        clearInterval(percentage);
                    }
                },
                error: function(){
                    console.log("ERROR: Request Failed to reach server");
                    clearInterval(percentage);
                }                

            });
        }, 100);
    })

})
