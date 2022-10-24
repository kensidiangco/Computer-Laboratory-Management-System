$(document).ready(function() {
    $(".ajaxRes").hide();
    setInterval(function() {
        $.ajax({
            url: "{% url 'getNotifs' %}",
            dataType: 'json',
            beforeSend:function() {
                $(".ajaxRes").show();
                $(".ajaxRes").text();
            },
            success:function(res) {
                _html='';
                _json = $.parseJSON(res.data);
                var monthNames = [
                    "Jan.", "Feb.", "March",
                    "Apr.", "May", "June", "July",
                    "Aug.", "Sept.", "Oct.",
                    "Nov.", "Dec."
                ];
                function addZero(i) {
                    if (i < 10) {
                        i = "0" + i;
                    }
                
                    return i;
                }
                function get_date(date){
                    var date = new Date(date);
                    var day = date.getDate();
                    var monthIndex = date.getMonth();
                    var year = date.getFullYear();
                    var hours = addZero(date.getHours());
                    var minutes = addZero(date.getMinutes());
                
                    return monthNames[monthIndex] + " " + day + " " + year;
                }
                
                $.each(_json, function(index, d) {
                    if(d.fields.read){
                        _html+='<a href="/schedule/request/'+ d.fields.sched_url +'" class="flex flex-col p-2 text-gray-600 hover:bg-gray-100 transition transition-delay-1 cursor-pointer"><span class="font-normal"><span class="font-bold">' + d.fields.notif_for + '</span>: <span class="text-sm">' + d.fields.description +'</span></span><span class="text-sm text-gray-400">'+ get_date(d.fields.date_created) +'<span></a>';
                    }else {
                        _html+='<a href="/schedule/request/'+ d.fields.sched_url +'" class="flex flex-col p-2 text-black hover:bg-purple-100 transition transition-delay-1 cursor-pointer"><span class="font-normal"><span class="font-bold">' + d.fields.notif_for + '</span>: <span class="text-sm">' + d.fields.description +'</span></span><span class="text-sm text-gray-400">'+ get_date(d.fields.date_created) +'<span class="float-right bg-blue-600 p-1.5 rounded-xl"></span><span></a>';
                    }
                    
                });

                $('.notif-list').html(_html);
                $(".ajaxRes").hide();
            }
        })
    }, 3000)
});

$(document).on("click", ".mark-all-read", function() {
    $.ajax({
        url: "{% url 'clearNotification' %}"
    });
});

$(document).ready(function() {
    $(".ajaxRes").hide();
    setInterval(function() {
        $.ajax({
            url: "{% url 'getNotifs' %}",
            dataType: 'json',
            beforeSend:function() {
                $(".ajaxRes").show();
                $(".ajaxRes").text();
            },
            success:function(res) {
                _totalUnread = '';
                _notifStatus='';
                _json = $.parseJSON(res.totalUnread);

                if(_json > 0) {
                    _notifStatus='<button type="button" class="text-sm pb-1 text-blue-500 cursor-pointer float-right w-full mark-all-read">Mark all as read</button>'
                    _totalUnread += '<button id="notification" onClick="notifClicked()" class="flex items-center">Notification <span class="bg-red-600 rounded-xl px-2 text-sm total-unread">'+ _json +'</span></button><button id="notification2" onClick="notifClicked2()" class="hidden flex items-center">Notification <span class="bg-red-600 rounded-xl px-2 text-sm total-unread">'+ _json +'</span></button> <button id="profile" onClick="profileClicked()">Account</button> <button id="profile2" onClick="profileClicked2()" class="hidden">Account</button>'
                } else {
                    _notifStatus='<p class="text-gray-600 text-sm text-center">No new updates.</p>'
                    _totalUnread += '<button id="notification" onClick="notifClicked()">Notification</button> <button id="notification2" onClick="notifClicked2()" class="hidden">Notification</button> <button id="profile" onClick="profileClicked()">Account</button> <button id="profile2" onClick="profileClicked2()" class="hidden">Account</button>'
                }

                $('.notif-status').html(_notifStatus);
                $('.total-unread').html(_totalUnread);
                $(".ajaxRes").hide();
            }
        })
    }, 3000)
});
