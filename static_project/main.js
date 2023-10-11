setTimeout(function() {
    for (let element of document.getElementsByClassName("alert")) {
        element.style.display = "none";
    }
}, 2000);

let cookie = document.cookie
let csrf_token = cookie.substring(cookie.indexOf('=') + 1)

function gebid(id) {
    return document.getElementById(id);
}

function go_to_url(url) {
    window.location.href = url;
}


function follower_user(btn, uid, url) {
        let post_data = {
            "leader_id": uid
        };


        $.ajax({
            type: "POST",
            url: url,
            data: JSON.stringify(post_data),
            headers: {
                "X-CSRFTOKEN": csrf_token
            },
            success: function() {
                console.log(post_data);
                if ($(btn).html().trim() === "Follow") {
                    $(btn).html("Following");
                } else {
                    $(btn).html("Follow");
                }
            },
            contentType: "application/json",
            dataType: "json"
        });
}

