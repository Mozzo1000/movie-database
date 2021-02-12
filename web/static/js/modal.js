var btn = document.querySelector('#open-modal');
var modalDlg = document.querySelector('#modal');
var imageModalCloseBtn = document.querySelector('#modal-close');
var imageModalCancelBtn = document.querySelector('#modal-cancel');

btn.addEventListener('click', function(){
  modalDlg.classList.add('is-active');
});

imageModalCloseBtn.addEventListener('click', function(){
  modalDlg.classList.remove('is-active');
});

imageModalCancelBtn.addEventListener('click', function(){
  modalDlg.classList.remove('is-active');
});