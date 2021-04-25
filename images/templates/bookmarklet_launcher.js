(function(){
  if (window.myBookmarklet !== undefined){
    myBookmarklet();
  }
  else {
  document.body.appendChild(
    document.createElement('script')
  ).src='https://c4b4a5bba490.ngrok.io/static/js/bookmarklet.js?r=' +
    Math.floor(Math.random()*99999999999999999999);
  }
})();

/* Актуальный код букмарклета будет находиться в файле bookmarklet.js. 
Это позволит обновлять выполняемый код без необходимости для пользователей
обновлять закладку, которую они добавили ранее. */
