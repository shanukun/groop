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



function like_post(btn, pid, url) {
    let post_data = {
        "post_id": pid,
    };
    let like_cnt_text = $(".like-cnt-" + pid);
    let num_likes = parseInt(like_cnt_text.html());
    $.ajax({
        type: "POST",
        url: url,
        data: JSON.stringify(post_data),
        headers: {
            "X-CSRFTOKEN": csrf_token
        },
        success: function(resp) {
            if (resp.add === 1) {
                $(btn).find("i").remove();
                $(btn).append("<i class='bi bi-heart-fill'></i>")
            } else {
                $(btn).find("i").remove();
                $(btn).append("<i class='bi bi-heart'></i>")
            }
            num_likes += resp.add;
            like_cnt_text.html(num_likes + " likes");
        },
        contentType: "application/json",
        dataType: "json"
    });
}

function delete_post(pid, url) {
    let post_data = {
        "post_id": pid,
    };

    $.ajax({
        type: "POST",
        url: url,
        data: JSON.stringify(post_data),
        headers: {
            "X-CSRFTOKEN": csrf_token
        },
        success: function() {
            location.reload();
        },
        contentType: "application/json",
        dataType: "json"
    });
}

function delete_comment(cid, url) {
    let comment_data = {
        "comment_id": cid,
    };

    $.ajax({
        type: "POST",
        url: url,
        data: JSON.stringify(comment_data),
        headers: {
            "X-CSRFTOKEN": csrf_token
        },
        success: function() {
            location.reload();
        },
        contentType: "application/json",
        dataType: "json"
    });
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

let post_selected_image = $("#post-selected-image");
function modal_focus(modal, tbox, is_c = false) {
    if (is_c) {
        modal.addEventListener("show.bs.modal", (e) => {
            pid = e.relatedTarget.dataset.pid;
            tbox.setAttribute("data-pid", pid)

        });
    }
    modal.addEventListener('shown.bs.modal', () => {
        tbox.focus()
    });
}

function create_post(url) {
    let form_data = new FormData($("#create-post-form")[0]);
    let image = $("#upload-post-image")[0].files[0];
    let post_body = $("#create-post-textbox").text();

    if (image === undefined && post_body.length <= 0) {
        return;
    }

    $("#create-toast").toast("show");

    if (image === undefined) {
        image = "";
    }
    form_data.append("image", image);
    form_data.append("body", post_body);

    $.ajax({
        type: "POST",
        url: url,
        data: form_data,
        headers: {
            "X-CSRFTOKEN": csrf_token
        },
        success: function(resp) {
            console.log(resp);
            $("#create-post-overlay").modal("hide");
            $("#post-toast").html("<span role='status'>Posted</span><a href='/posts/" + resp.post_id + "'>View</a>");
        },
        contentType: false,
        processData: false
    });
}

function create_comment(url) {
    let form_data = new FormData($("#create-comment-form")[0]);
    let comment_body = $("#create-comment-textbox").text();
    let pid = parseInt($("#create-comment-textbox").data("pid"));

    $("#create-toast").toast("show");

    form_data.append("body", comment_body);
    form_data.append("post_id", pid);

    $.ajax({
        type: "POST",
        url: url,
        data: form_data,
        headers: {
            "X-CSRFTOKEN": csrf_token
        },
        success: function(resp) {
            console.log(resp);
            $("#create-comment-overlay").modal("hide");
            $("#post-toast").html("<span role='status'>Posted</span><a href='/posts/" + resp.post_id + "'>View</a>");
        },
        contentType: false,
        processData: false
    });
}

$("#upload-post-image").on("change", function() {
    let filename = $(this).val().split("\\");
    filename = filename[filename.length - 1];
    post_selected_image.html(filename);
});
