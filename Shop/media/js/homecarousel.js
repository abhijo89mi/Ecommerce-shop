function mycarousel_initCallback(carousel)
{
    carousel.buttonNext.bind('click', function() {
        carousel.startAuto(5);
    });

    carousel.buttonPrev.bind('click', function() {
        carousel.startAuto(5);
    });

    // Pause autoscrolling if the user moves with the cursor over the clip.
    carousel.clip.hover(function() {
        carousel.stopAuto();
    }, function() {
        carousel.startAuto();
    });
};

jQuery(document).ready(function() {
    jQuery('#mycarousel').jcarousel({
        auto: carousel_autoplay,
        wrap: 'last',
        visible: carousel_items_visible,
        scroll: carousel_scroll,
        initCallback: mycarousel_initCallback
    });
});