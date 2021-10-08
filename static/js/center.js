function change(obj) {
    var value = $(obj).find('option:selected').text();
    $('#datashow').val(value);
}
