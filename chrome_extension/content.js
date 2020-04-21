var xhr = new XMLHttpRequest();
var url = 'https://us-central1-opty-274801.cloudfunctions.net/optimistic_analysis';


// 純粋な検索結果を取得
const articlesElms = getElms('g');
const articleTexts = extractTexts(articlesElms);
// ニュースを取得
const newsElms = getElms('So9e7d');
const newsTexts = extractTexts(newsElms);
// PN評価をしてスタイル変更
computeScoresAndChangeStyles([{'elms': articlesElms, 'texts': articleTexts}, {'elms': newsElms, 'texts': newsTexts}]);


function computeScoresAndChangeStyles(targetsList) {
  // レスポンス
  xhr.onload = function(e) {
    if (xhr.status === 200) {
      const scoresList = JSON.parse(xhr.responseText);
      scoresList.forEach((scores, i) => {
        changeStyles(targetsList[i]['elms'], scores);
      });
    }
  }
  xhr.onerror = function(e) {
    console.error(xhr.statusText);
    return;
  }
  xhr.onabort = function(e) {
    console.error(xhr.statusText);
    return;
  }
  xhr.ontimeout = function(e) {
    console.error(xhr.statusText);
    return;
  }
  // リクエスト
  xhr.open('POST', url, true);
  xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  xhr.send(JSON.stringify(targetsList));
}

function changeStyles(elms, scores) {
  if (scores === undefined) { return }
  // PN評価値を用いてスタイル変更
  for (let i = 0; i < scores.length; i++) {
    const elm = elms[i], score = scores[i];
    if (score >= 0) {
      const style = `transition: filter 1s; filter: blur(0);`;
      elm.setAttribute("style", style);
    } else {
      const style = `transition: filter 1s; filter: blur(${-score * 50}px);`;
      elm.setAttribute("style", style);
    }

  }
}

function getElms(className) {
  return Array.prototype.filter.call(document.getElementsByClassName(className), function(e) {
    if (e.className == className) {
      return e;
    }
  });
}

function extractTexts(elms) {
  return Array.prototype.map.call(elms, function(e) {
    return e.textContent;
  });
}
