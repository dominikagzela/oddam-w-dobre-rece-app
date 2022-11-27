document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;
      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");
        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;
      this.$categories = form.querySelectorAll('.data-categories-id');
      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      const ourCategories = []
      const ourCategoriesNames = []
      let ourCategoriesString = ''
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          if(this.currentStep === 2) {
             this.$categoriesCheckboxes = form.querySelectorAll('.category-input:checked')
            this.$categoriesCheckboxes.forEach((checkbox) => {
              ourCategories.push(parseInt(checkbox.value)) // CATEGORIES
              ourCategoriesNames.push(checkbox.nextElementSibling.nextElementSibling.innerHTML)
            });
            this.$categories.forEach((item) => {
            const currentCategoryID = parseInt(item.dataset['category'])
            if (ourCategories.includes(currentCategoryID)){
              const currentInstitutionID = item.dataset['institution']
              document.getElementById(currentInstitutionID).style.display = 'block'
            }
          })
          }
          if(this.currentStep === 3) {
            this.$quantity = form.querySelector('[name="quantity"]'); // BAGS
          }
          if(this.currentStep === 4) {
            this.$institution = form.querySelector('.institution-input:checked'); // INSTITUTION
          }
          if(this.currentStep === 5) {
            this.$street = form.querySelector('[name="address"]'); // STREET
            this.$city = form.querySelector('[name="city"]'); // CITY
            this.$zip_code = form.querySelector('[name="zip_code"]'); // POSTCODE
            this.$phone_number = form.querySelector('[name="phone_number"]'); // NUMBER PHONE
            this.$data = form.querySelector('[name="pick_up_date"]'); // DATE
            this.$time = form.querySelector('[name="pick_up_time"]'); // TIME
            this.$more_info = form.querySelector('[name="pick_up_comment"]'); // MORE INFO

            ourCategoriesNames.forEach((item, key) => {
            if(key !== ourCategoriesNames.length - 1) {
              ourCategoriesString = ourCategoriesString + item + ', '
            } else {
              ourCategoriesString = ourCategoriesString + item
            }
          })

            form.querySelector('.icon-bag').nextElementSibling.textContent=
                ('Worki: '+ this.$quantity.value + ' (' + ourCategoriesString + ')');
            form.querySelector('.icon-hand').nextElementSibling.textContent=
                ('Dla: '+ this.$institution.value);

            const addressInfo = form.querySelector('.address-info').children
            addressInfo[0].innerHTML = this.$street.value
            addressInfo[1].innerHTML = this.$city.value
            addressInfo[2].innerHTML = this.$zip_code.value
            addressInfo[3].innerHTML = this.$phone_number.value

            const receiptInfo = form.querySelector('.receipt-info').children
            receiptInfo[0].innerHTML = this.$data.value
            receiptInfo[1].innerHTML = this.$time.value
            receiptInfo[2].innerHTML = this.$more_info.value
          }

          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          if(this.currentStep === 2) {
            document.querySelector('.institution').style.display = 'none'
          }
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;
      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      if(this.currentStep < 5 ){
              e.preventDefault();
      this.currentStep++;
      this.updateForm();
      }
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
