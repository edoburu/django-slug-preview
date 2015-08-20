!function($){
  var base_url = location.protocol + "//" + location.host;

  function onReady() {
    $("kbd.slugpreview").each(function (i, field) {
      var $field = $(field);

      $field.find('input').change(onInputChange);

      // When the hostname is not included yet in the form,
      // include the current hostname to the field.
      var $prefix = $field.find('.url-prefix');
      var prefix = $prefix.text();
      if(prefix.indexOf('://') == -1)
        $prefix.text(base_url + prefix);
    });
  }

  function onInputChange(event) {
    // Update the text preview.
    $(this).closest('kbd.slugpreview').find('.url-slug-text').text(this.value);
  }

  onReady();  // try directly.
  $.fn.ready(onReady);

}(window.jQuery || window.django.jQuery);
