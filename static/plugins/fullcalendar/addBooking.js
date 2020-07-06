$(document).ready(function () {

    // Get the modal
    var modal = document.getElementById("addEventsModal");


    // Get the Add Event button
    var addEvent = document.getElementById("add-e");
    // Get the Edit Event button
    var editEvent = document.getElementById("edit-event");
    // Get the Discard Modal button
    var discardModal = document.querySelectorAll("[data-dismiss='modal']")[0];

    // Get the Add Event button
    var addEventTitle = document.getElementsByClassName("add-event-title")[0];
    // Get the Edit Event button
    var editEventTitle = document.getElementsByClassName("edit-event-title")[0];

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // Get the all <input> elements insdie the modal
    var input = document.querySelectorAll('input[type="text"]');
    var radioInput = document.querySelectorAll('input[type="radio"]');

    // Get the all <textarea> elements insdie the modal
    var textarea = document.getElementsByTagName('textarea');

    // Create BackDrop ( Overlay ) Element
    function createBackdropElement() {
        var btn = document.createElement("div");
        btn.setAttribute('class', 'modal-backdrop fade show')
        document.body.appendChild(btn);
    }

    // Reset radio buttons

    function clearRadioGroup(GroupName) {
        var ele = document.getElementsByName(GroupName);
        for (var i = 0; i < ele.length; i++)
            ele[i].checked = false;
    }

    // Reset Modal Data on when modal gets closed
    function modalResetData() {
        modal.style.display = "none";
        for (i = 0; i < input.length; i++) {
            input[i].value = '';
        }
        for (j = 0; j < textarea.length; j++) {
            textarea[j].value = '';
            i
        }
        clearRadioGroup("marker");
        // Get Modal Backdrop
        var getModalBackdrop = document.getElementsByClassName('modal-backdrop')[0];
        document.body.removeChild(getModalBackdrop)
    }


    // Clear Data and close the modal when the user clicks anywhere outside of the modal.
    window.onclick = function (event) {
        if (event.target == modal) {
            modalResetData();
            document.getElementsByTagName('body')[0].removeAttribute('style');
        }
    }

    newDate = new Date()
    monthArray = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    function getDynamicMonth(monthOrder) {
        var getNumericMonth = parseInt(monthArray[newDate.getMonth()]);
        var getNumericMonthInc = parseInt(monthArray[newDate.getMonth()]) + 1;
        var getNumericMonthDec = parseInt(monthArray[newDate.getMonth()]) - 1;

        if (monthOrder === 'default') {

            if (getNumericMonth < 10) {
                return '0' + getNumericMonth;
            } else if (getNumericMonth >= 10) {
                return getNumericMonth;
            }

        } else if (monthOrder === 'inc') {

            if (getNumericMonthInc < 10) {
                return '0' + getNumericMonthInc;
            } else if (getNumericMonthInc >= 10) {
                return getNumericMonthInc;
            }

        } else if (monthOrder === 'dec') {

            if (getNumericMonthDec < 10) {
                return '0' + getNumericMonthDec;
            } else if (getNumericMonthDec >= 10) {
                return getNumericMonthDec;
            }
        }
    }

    /* initialize the calendar
    -----------------------------------------------------------------*/

    var calendar = $('#addCalendarBooking').fullCalendar({
        themeSystem: 'bootstrap4',
        selectable: true,
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay,listMonth'
        },
        weekNumbers: true,

        eventLimit: true, // allow "more" link when too many events
        events: 'https://fullcalendar.io/demo-events.json',
        dateClick: function (info) {
            alert('clicked ' + info.dateStr);
        },
        select: function (info) {
            alert('selected ' + info.startStr + ' to ' + info.endStr);
        },
        render: true,
    })


    function enableDatePicker() {
        var startDate = flatpickr(document.getElementById('start-date'), {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
            minDate: new Date()
        });

        var abv = startDate.config.onChange.push(function (selectedDates, dateStr, instance) {

            var endtDate = flatpickr(document.getElementById('end-date'), {
                enableTime: true,
                dateFormat: "Y-m-d H:i",
                minDate: dateStr
            });
        })

        var endtDate = flatpickr(document.getElementById('end-date'), {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
            minDate: new Date()
        });
    }


    function randomString(length, chars) {
        var result = '';
        for (var i = length; i > 0; --i) result += chars[Math.round(Math.random() * (chars.length - 1))];
        return result;
    }


});