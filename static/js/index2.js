var $ = function( id ) {
    return document.getElementById( id ); 
};



let showMeta = document.getElementById("js-data-hub").dataset,
    showId = showMeta.showId,
    showName = showMeta.showName,
    userRating = parseFloat(showMeta.userRating) || 0,
    userPost = document.getElementById("review_text") ? document.getElementById("review_text").innerText : '',
    reviewId = showMeta.reviewId || null;



if ( userRating > 0  ){
    document.querySelector(`input[value="${userRating}"]`).checked = true;
    document.getElementById("rating_box").classList.toggle("rating--submitted");
}

document.execCommand("defaultParagraphSeparator", false, "div");

document.getElementById("js-user-review").addEventListener('click', function(e){
    if (event.target.matches('#btn_editor')){
        editReview(e);
    }else if (event.target.matches('#btn_save')){
        saveReview(e)
    }else if (event.target.matches('#btn_submit')){
        addReview(e);
    }else if (event.target.matches('#btn_delete')){
        deletePrompt(e);
    }else{
        return ;
    }
}, true);
    
function deletePrompt(){
    $('delete-prompt').style.display = 'block';
};

function cancelDelete(){
    $('delete-prompt').style.display = 'none';
};


function addReview(e){
    e.preventDefault();
    userPost =  document.getElementById("review_text").innerText.trim();
    if (document.querySelector('input[name="rating"]:checked') !== null){
        userRating = document.querySelector('input[name="rating"]:checked').getAttribute('value');
    };
    if (userRating === 0){
        document.getElementById("rating_input_warning").innerText = `Rate ${showName} for a tldr; version of your review`;
        return ;
    };
    let data = {
        id      : showId,
        post    : userPost,
        rating  : userRating
    };
    fetch('http://localhost:8000/add_review/', {
        method: 'post',
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken" : getcsrf('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(data)
    }).then(function(response) {
        return response.json();
    }).then(function(data) {
        debugger;
        document.getElementById("review_text").setAttribute("contenteditable", false);
        document.getElementById("btn_submit").classList.toggle('hide');
        document.getElementById("btn_editor").classList.toggle('hide');
        document.getElementById("btn_delete").classList.toggle('hide');
        reviewId = data.newReviewID
        document.getElementById("rating_box").classList.toggle("rating--submitted")

        
        // formattedPost = createParagraphs(this.data.post)
        // document.getElementById("review_text").innerHTML = formattedPost
    }).catch(function(e) {
        console.log(e); 
    });
};


function saveReview(e){
    userPost =  document.getElementById("review_text").innerText;
    if (document.querySelector('input[name="rating"]:checked') !== null){
        userRating = document.querySelector('input[name="rating"]:checked').getAttribute('value');
    }    
    if (userRating === 0){
        document.getElementById("rating_input_warning").innerText = `Rate ${showName} for a tldr; version of your review`;
        return ;
    }
    let data = {
        id      : reviewId,
        post    : userPost,
        rating  : userRating
    };
    
    fetch('http://localhost:8000/save_review/', {
        method: 'post',
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken" : getcsrf('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(data)
    }).then(function(response) {
        return response.json();
    }).then(function(data) {
        // let editor = document.getElementById("review_editor")
        // document.getElementById("user_review_form").classList.toggle("hide")
        // formattedPost = createParagraphs(this.data.post)
        // document.getElementById("user_review_form").remove()
        // document.getElementById("review_text").innerHTML = formattedPost
        // document.getElementById("user-submitted-review").classList.toggle("hide");
        editor.setAttribute("placeholder", "You can add a review if you like...")
    }).catch(function(e) {
        console.log(e); 
    });
    document.getElementById("btn_editor").classList.toggle('hide');
    document.getElementById("btn_delete").classList.toggle('hide');
    document.getElementById("btn_save").classList.toggle('hide');
    document.getElementById("rating_box").classList.toggle("rating--submitted");
    let editor = document.getElementById("review_text");
    editor.setAttribute("contenteditable", false);
};

function editReview(e){
    let editor = document.getElementById("review_text");
    editor.setAttribute("contenteditable", true);
    var range = document.createRange();
    var sel = window.getSelection();
    nodeLength = editor.childNodes.length - 1 > 0 ? editor.childNodes.length - 1 : 0;
    if (nodeLength<=0){
        range.setStart(editor, editor);
    }else{
        range.setStart(editor.childNodes[nodeLength], editor.childNodes[nodeLength]);
    }
    range.collapse(true);
    sel.removeAllRanges();
    sel.addRange(range);
    editor.focus(); 

    document.getElementById("btn_editor").classList.toggle('hide');
    document.getElementById("btn_delete").classList.toggle('hide');
    editor.setAttribute("placeholder", "Add Review...");

    document.getElementById("rating_box").classList.toggle("rating--submitted")


    let save_button =  document.getElementById("btn_save")
    save_button.classList.toggle('hide');
    // save_button.disabled = true
}


function deleteReview(e){
    let data = {
        id      : reviewId,
    };
    fetch('http://localhost:8000/delete_review/', {
        method: 'post',
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken" : getcsrf('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(data)
    }).then(function(response){
        return response.text()
    }).then(function(data){
        // formNode = document.getElementById('user-submitted-review')
        // while (formNode.firstChild) {
        //     formNode.removeChild(formNode.firstChild);
        // }
        $('delete-prompt').style.display = 'none'
        $('user_review_form').reset()
        let editor = $('review_text')
        editor.innerText = ''
        editor.setAttribute("contenteditable", true);
        editor.setAttribute("placeholder","You can add a review if you like...")
        $('user-like-count').innerHTML = 0
        document.getElementById("btn_delete").classList.toggle('hide');
        document.getElementById("btn_editor").classList.toggle('hide');
        document.getElementById("btn_submit").classList.toggle('hide');
        document.getElementById("rating_box").classList.toggle("rating--submitted")
        // target = document.getElementById('user-submitted-review')
        // target.insertAdjacentHTML('beforeend', editReviewBlock)
        // 
    }).catch(function(e){
        console.log(e);
    })

}

document.getElementById('js-review__target').addEventListener('click', function(e){
    if (event.target.matches('.like__btn')){
        reviewLikes(e);
    }
});

function reviewLikes(e){
    el = e.target;
    likedReview = el.dataset.reviewId;
    data = {
        reviewId : likedReview
    };
    fetch('http://localhost:8000/toggle_likes/', {
        method: 'post',
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken" : getcsrf('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(data)
    }).then(function(response){
        if (response.redirected){
            document.querySelector(".signin-wrapper").style.display= "block";
            return ;
        };
        response.json().then(function(data){
            el.classList.toggle('like__btn--active');
            let likeValue = parseInt(el.nextElementSibling.innerText)
            if (data.userAction===1){
                el.nextElementSibling.innerText = likeValue + 1
            }else{
                el.nextElementSibling.innerText = likeValue - 1
            };
        })
        
    }).catch(function(e){
        console.log(e)
    })

}



function formSubmit(e){
    debugger;
    // el = e.target;
    // likedReview = el.dataset.reviewId;
    // data = {
    // fetch('http://localhost:8000/toggle_likes/', {
    //     method: 'post',
    //     credentials: 'same-origin',
    //     headers: {
    //         "X-CSRFToken" : getcsrf('csrftoken'),
    //         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    //         'X-Requested-With': 'XMLHttpRequest'
    //     },
    //     body: JSON.stringify(data)
    // }).then(function(response){
    //     if (response.redirected){
    //         document.querySelector(".signin-wrapper").style.display= "block";
    //         return ;
    //     };
    //     response.json().then(function(data){
            
    //         el.classList.toggle('like__button-active');
    //         let likeValue = parseInt(el.nextElementSibling.innerText)
    //         if (data.userAction===1){
    //             el.nextElementSibling.innerText = likeValue + 1
    //         }else{
    //             el.nextElementSibling.innerText = likeValue - 1
    //         };
    //     })
        
    // }).catch(function(e){
    //     console.log(e)
    // })

}

let page = 2;
function loadMoreReviews(id){
    let appendTargetEl = document.getElementById("review_target")
    fetch(`http://localhost:8000/paginate_reviews/${id}?page=${page}`)
    .then(function(response) {
	    return response.json();
    }).then(function(data) {
        parsedData = JSON.parse(data.paginated_reviews)
        for( let i = 0 ; i < parsedData.length; i++ ){
            createReviewBlock(parsedData[i], appendTargetEl)
        }
        if (!data.next_page){
            buttonActions = document.getElementById("review_paginator")
            buttonActions.disabled = true
            buttonActions.innerText = "You have read all the reviews, Chingu!"
        }
        page++
    }).catch(function(e) {
        console.log(e)
    })
}



function createReviewBlock(review, target){
    let reviewPost = review.post;
    let reviewBlock = `			
    <div class="other-review__each">
        <div class="other-review__profile">
            <a href=""><img src="${review.avatar}"></a>
        </div>
        <div class="review__info">
            <span class="other-review__name"><a href="">${review.user}</a></span>
            <span class="drama__rating">${review.rating}</span>
            <div class="other-review__text">
                ${reviewPost}
            </div>
            <div class="other-review-actions">
                <div class="other-review__report">
                </div>
                <div class="other-review__like">
                    <div class="like__button"></div>
                    <div class="like__count">${review.likes}</div>
                </div>
            </div>
        </div>
    </div>
    `;
    target.insertAdjacentHTML('beforeend', reviewBlock);
}

function createParagraphs(post){
    textBreaks = post.split('\n');
    para = "";
    for ( let i = 0; i < textBreaks.length; i++){
        if(textBreaks[i].trim()){
            block = '<p>' + textBreaks[i] + '</p>';
            para += block;
        };
    };
    return para;
}


function getcsrf(name){
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                };
        };
    };
    return cookieValue;
};



document.getElementsByClassName("drama__videos")[0].addEventListener('click', function(e){
    if (event.target.matches('.drama_poster_link') || event.target.matches('.drama__poster__playbutton')){
        openPlayer(e.target.dataset.ylink)
    }
})

function openPlayer(link){
    let getFrame = document.getElementById("video")
    getFrame.style.display = 'block'
    getFrame.querySelector('div > iframe').src = `https://www.youtube.com/embed/${link}`
}

function closeplayer(){
    let getFrame = document.getElementById("video")
    getFrame.style.display = 'none'
    getFrame.querySelector('div > iframe').src = ``
}


function opensignin(){
    document.querySelector(".signin-wrapper").style.display= "block";
}
function closesignin(){
    document.querySelector(".signin-wrapper").style.display= "none";
}
function openfeedback(){
    document.querySelector(".feedback-wrapper").classList.toggle("hide");
}
function closefeedback(){
    document.querySelector(".feedback-wrapper").classList.toggle("hide");
}

[...document.getElementsByClassName('info__header__heading')].forEach((elm)=> elm.addEventListener("click", infoTabs))
function infoTabs(){
    document.getElementsByClassName('info__header__heading--active')[0].classList.remove("info__header__heading--active");
    this.classList.add('info__header__heading--active');
    document.getElementsByClassName("drama-info--active")[0].classList.remove("drama-info--active");
    let getid= this.getAttribute("show");
    document.getElementById(getid).classList.add("drama-info--active");
}