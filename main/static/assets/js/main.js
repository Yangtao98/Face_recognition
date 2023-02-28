

(function () {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function (e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

  /**
   * Search bar toggle
   */
  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function (e) {
      select('.search-bar').classList.toggle('search-bar-show')
    })
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }



  /**
   * Initiate Bootstrap validation check
   */
  var needsValidation = document.querySelectorAll('.needs-validation')

  Array.prototype.slice.call(needsValidation)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

  /**
   * Initiate Datatables
   */
  const datatables = select('.datatable', true)
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable);
  })

  /**
   * Autoresize echart charts
   */
  const mainContainer = select('#main');
  if (mainContainer) {
    setTimeout(() => {
      new ResizeObserver(function () {
        select('.echart', true).forEach(getEchart => {
          echarts.getInstanceByDom(getEchart).resize();
        })
      }).observe(mainContainer);
    }, 200);
  }


  var imgWrap = "";
  var imgArray = [];

  $('.upload__inputfile').each(function () {
    $(this).on('change', function (e) {
      imgWrap = $(this).closest('.upload__box').find('.upload__img-wrap');
      var maxLength = $(this).attr('data-max_length');

      var files = e.target.files;
      var filesArr = Array.prototype.slice.call(files);
      var iterator = 0;
      filesArr.forEach(function (f, index) {

        if (!f.type.match('image.*')) {
          return;
        }

        if (imgArray.length > maxLength) {
          return false
        } else {
          var len = 0;
          for (var i = 0; i < imgArray.length; i++) {
            if (imgArray[i] !== undefined) {
              len++;
            }
          }
          if (len > maxLength) {
            return false;
          } else {
            imgArray.push(f);

            var reader = new FileReader();
            reader.onload = function (e) {
              var html = "<div class='upload__img-box'><div style='background-image: url(" + e.target.result + ")' data-number='" + $(".upload__img-close").length + "' data-file='" + f.name + "' class='img-bg'><div class='upload__img-close'></div></div></div>";
              imgWrap.append(html);
              iterator++;
            }
            reader.readAsDataURL(f);
          }
        }
      });
    });
  });

  $('body').on('click', ".upload__img-close", function (e) {
    var file = $(this).parent().data("file");
    for (var i = 0; i < imgArray.length; i++) {
      if (imgArray[i].name === file) {
        imgArray.splice(i, 1);
        break;
      }
    }
    $(this).parent().parent().remove();
  });




})();






$('#status').on('change', function () {
  let status = document.getElementById("status").value;
  if (status == "Pending") {

    let option2 = '<option value="" selected disabled>Choose</option>';
    let option1 = '<option value="" selected disabled>Choose</option>';

    for (let i = 0; i < 25; i++) {
      // value day number with 0. 01 02 03 04..
      let day = (i <= 9) ? '0' + i : i;

      // or value day number 1 2 3 4..
      // let day = i;
      if (i == 24) {
        option1 += '<option value=23:59>23:59</option>';
        option2 += '<option value=23:59>23:59</option>';

      } else {
        option1 += '<option value="' + day + ':00"' + '>' + day + ':00</option>';
        option1 += '<option value="' + day + ':30"' + '>' + day + ':30</option>';
        option2 += '<option value="' + day + ':00"' + '>' + day + ':00</option>';
        option2 += '<option value="' + day + ':30"' + '>' + day + ':30</option>';
      }
    }
    document.getElementById("timestartnew").innerHTML = option1;
    document.getElementById("timeendnew").innerHTML = option2;
    document.getElementById("timechange").style.display = "block";
    //document.getElementById("timenone").style.display = "none";
    document.getElementById("timestartnew").setAttribute('required', '');
    document.getElementById("timeendnew").setAttribute('required', '');
  }
  // else if (status == "halfday") {
  //   let option3 = '<option value="" selected disabled>Choose</option>';
  //
  //   for (let i = 0; i < 25; i++) {
  //     // value day number with 0. 01 02 03 04..
  //     let day = (i <= 9) ? '0' + i : i;
  //
  //     // or value day number 1 2 3 4..
  //     // let day = i;
  //     if (i == 24) {
  //       option3 += '<option value=23:59>23:59</option>';
  //     } else {
  //       option3 += '<option value="' + day + ':00"' + '>' + day + ':00</option>';
  //       option3 += '<option value="' + day + ':30"' + '>' + day + ':30</option>';
  //     }
  //}
  //   document.getElementById("timeendnew2").innerHTML = option3;
  //   document.getElementById("timenone").style.display = "block";
  //   document.getElementById("timechange").style.display = "none";
  // }
  else {
    // document.getElementById("timenone").style.display = "none";
    document.getElementById("timechange").style.display = "none";
    document.getElementById("timestartnew").removeAttribute('required');
    document.getElementById("timeendnew").removeAttribute('required');
  }
});


/**
   * check password
   */
function matchpassword() {
  var password = document.getElementById("newPassword")
    , confirm_password = document.getElementById("renewPassword");

  if (password.value != confirm_password.value) {
    alert("Passwords Don't Match");
  }



}