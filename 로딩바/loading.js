function clickedBtn(){
    // 로딩 표시
    showLoading();
    // 로딩 숨기기(5초 후)
    setTimeout("hideLoading()", 5000);
  }
  function showLoading(){
    $("#roadingStatus").show();
  }
  function hideLoading(){
    $("#roadingStatus").hide();
  }
  