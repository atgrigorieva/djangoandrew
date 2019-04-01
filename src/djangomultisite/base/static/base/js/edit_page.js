$(".type-element").each((i, elem) => {
    $(elem).on("click", (e) => {
        addElement(elem);
    })
});

$(".element").each((i, elem) => {
    $(elem).on("click", (e) => {
        showAttributs(elem);
    })
});

$(".close").each((i, elem) => {
    $(elem).on("click", (e) => {
        removeElement(elem);
        e.stopPropagation();
    })
});

function addElement(elem) {
    let elemId = $(elem).data("id");
    let pageId = $(".settings").data("id");

    $.post({
        url: `/add_element/${elemId}/to/${pageId}/`,
        dataType: "json",
        success: (data) => {
            let html = `
                <div class="element" data-id="${data.element.id}">
                    ${data.element.name}
                    <button type="button" class="close" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                </div>`;

            $('.elements').append(html);
            let element = $(`.element[data-id=${data.element.id}]`);

            element.on("click", (e) => {
                showAttributs(element);
            });

            element.find('.close').on("click", (e) => {
                removeElement(element.find('.close'));
                e.stopPropagation();
            })

            showAttributs(element)
        }
    });
}

function showAttributs(elem) {
    let elemId = $(elem).data("id");

    $.get({
        url: `/get_attributs/${elemId}/`,
        dataType: "json",
        success: (data) => {
            $('.attributs').empty();
            data.attributs.forEach((attribut) => {
                let html = `
                    <label for="${attribut.name}" class="col-sm-2 col-form-label">${attribut.name}</label>
                    <div class="col-sm-10">
                        <input class="form-control"
                            id="${attribut.name}"
                            type="${attribut.hasValue ? "text" : "checkbox"}"
                            name="${attribut.name}"
                            ${attribut.value ? `value="${attribut.value}"` : ""}
                        >
                    </div>
                `;
                $('.attributs').append(html);

                $(`input[id=${attribut.name}]`).on('focusout', (e) => {
                    updateElement($(`.page #${elemId}`), attribut.name, event.target.value);
                    saveAttributs(elem);
                });

                $(`input[id=${attribut.name}]`).on('keypress', (e) => {
                    if(e.which == 13) {
                        updateElement($(`.page #${elemId}`), attribut.name, event.target.value);
                        saveAttributs(elem);
                    }
                });
            })
        }
    });
}

function saveAttributs(elem) {
    let elemId = $(elem).data("id");
    let data = {};
    let attributs = $('.attributs input');

    for (let i = 0; i < attributs.length; i++) {
        data[attributs[i].getAttribute("id")] = attributs[i].value;
    }

    $.post({
        url: `/update_element/${elemId}/`,
        dataType: "json",
        data,
        success: (data) => {
            null;
        }
    });
}

function removeElement(elem) {
    let parent = $(elem).parent()
    let elemId = parent.data("id");

    $('.attributs').empty();

    $.post({
        url: `/remove_element/${elemId}/`,
        dataType: "json",
        success: (data) => {
            parent.remove();
            $(`.page #${elemId}`).remove();
        }
    });
}

$.get({
    url: `/get_html/${$('.settings').data('id')}`,
    success: (data) => {
        $('.page').append(data);
    }
});

function updateElement(elem, attribut, value) {
    if (attribut === 'inner_html' ) {
        $(elem).html(value);
    }
    else {
        $(elem).attr(attribut, value);
    }
}