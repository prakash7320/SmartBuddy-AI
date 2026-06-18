const chatBox = document.getElementById("chatBox");
const imageInput = document.getElementById("imageInput");
const textInput = document.getElementById("textInput");
const preview = document.getElementById("preview");
const micBtn = document.getElementById("micBtn");


// IMAGE PREVIEW

imageInput.onchange = () => {

    const file = imageInput.files[0];

    if(file){

        preview.src = URL.createObjectURL(file);

        preview.style.display = "block";
    }
};


// ENTER SEND

textInput.addEventListener("keydown", function(e){

    if(e.key === "Enter" && !e.shiftKey){

        e.preventDefault();

        sendMessage();
    }

});


// NEWS FUNCTION

async function getNews(){

    try{

        const response = await fetch(
            "http://127.0.0.1:8000/news"
        );

        const data = await response.json();


        // AI NEWS MESSAGE

        const newsMsg = document.createElement("div");

        newsMsg.className = "message ai";

        newsMsg.innerText = data.news;

        chatBox.appendChild(newsMsg);

        chatBox.scrollTop = chatBox.scrollHeight;

    }catch(error){

        const err = document.createElement("div");

        err.className = "message ai";

        err.innerText = "News loading failed";

        chatBox.appendChild(err);
    }
}



// SEND MESSAGE

async function sendMessage(){

    const text = textInput.value.trim();

    const file = imageInput.files[0];

    if(!text && !file) return;


    // HIDE TITLE

    document.getElementById("title").style.display = "none";

    chatBox.style.display = "block";



    // USER TEXT

    if(text){

        const userMsg = document.createElement("div");

        userMsg.className = "message user";

        userMsg.innerText=text;

        chatBox.appendChild(userMsg);
    }



    // USER IMAGE

    if(file){

        const img = document.createElement("img");

        img.src = URL.createObjectURL(file);

        img.style.width = "120px";

        img.style.borderRadius = "10px";


        const wrapper = document.createElement("div");

        wrapper.className = "message user";

        wrapper.appendChild(img);

        chatBox.appendChild(wrapper);
    }



    // AI THINKING

    const aiMsg = document.createElement("div");

    aiMsg.className = "message ai";

    aiMsg.innerText = "Thinking..."

    chatBox.appendChild(aiMsg);

    chatBox.scrollTop = chatBox.scrollHeight;



    // SEND TO BACKEND

    const formData = new FormData();

    formData.append("text", text);

    if(file){

        formData.append("image", file);
    }



    try{

        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        aiMsg.innerText = data.reply;

    }catch(error){

        aiMsg.innerText = "Server error. Try again.";
    }



    // RESET

    textInput.value = "";

    imageInput.value = "";

    preview.style.display = "none";
}



// 🎤 VOICE INPUT

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


if(SpeechRecognition){

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.continuous = false;

    recognition.interimResults = false;



    // SPEECH RESULT

    recognition.onresult = function(event){

        const voiceText =
            event.results[0][0].transcript;

        textInput.value = voiceText;
    };



    // MIC CLICK

    micBtn.addEventListener("click", () => {

        recognition.start();

    });

}else{

    alert("Voice input not supported");

}
