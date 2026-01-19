// 1. 반복문 - 짝수 출력
// 1부터 10까지 중 짝수만 콘솔에 출력하세요.

// 1부터란 의미에는 맞지않는 방법
// for (let i = 2; i < 11; i += 2) {
//     console.log(i);
// }

for (let i = 1; i < 11; i++) {  // i를 1부터 10까지 1씩 증가
    if (i % 2 === 0)  // 2로 나눈 나머지가 0이면 짝수
        console.log(i);  // 짝수만 출력
}

// for (let i = 1; 1 < 11; 1++) {      //무한루프
//     if (i % 2 === 0) {
//         console.log(i);
//     }
// }

// 2. 배열 순회 (for...of)
let fruits = ['apple', 'banana', 'cherry']  // 배열 선언

for (const fruit of fruits) {  // 배열의 각 요소를 fruit에 담아서 반복
    console.log(fruit);  // 각 과일 이름 출력
}

// 3. 객체 (Object)
let user = {  // 객체 선언 (key: value 형태)
    name: "Alice",  // 이름
    age: 30,  // 나이
    email: "alice@example.com"  // 이메일
}
//위가 바로 객체임, 이름을 적어서 관리하는거

console.log(user.name);  // 객체.속성명으로 접근
console.log(user.age);  // 30 출력
console.log(user.email);  // 이메일 출력

// 4. 함수와 return
// 함수 선언.    #불합격만 표시, 값이 없지만 리턴(실행할게 없어짐)에서 끝나서.
// function checkPass(score) {
//     if (score >=60)  {
//         return "합격";
//     } else {
//         return "불합격";
//     }
// }

// let result = checkPass()
// console.log(result);




// #불합격도 표시되고, undefined도 표시됨. 리턴이 디폴트 리턴(실행할게 없을때)까지 가서.
function checkPass(score) {  // 점수를 받아 합격/불합격 판정
    if (score >= 60) {  // 60점 이상이면
        console.log("합격");  // 합격 출력
    } else {  // 60점 미만이면
        console.log("불합격");  // 불합격 출력
    }
}  // return이 없으면 undefined 반환됨

let result = checkPass(70)  // 70점으로 함수 호출 → "합격" 출력
console.log(result);  // undefined 출력 (return이 없어서)

// 리턴에 따른 undefined값은, 파이썬에선 보지 못했던 부분이라 처음엔 생소했는데, 풀어보자면,

// 리턴이란게 사실 디폴트값으로 들어가 있단다. 그래서 우리가 예를 들면 위에 checkPass(70)에서도 프린트 되는거(합격)랑은 별개로  쭉 컴퓨터가 일하다가 일단 리턴이 되긴한다(undefined). 여기서 왜 undefined가 나올까? 이유는 디폴트 리턴이 사용될때에는 우리가 값을 안넣은것으로 얘가 생각하기 때문에 일단 오류 안내고 결과값은 반환해줄게. 근데 너 값을 안넣었드라(undefined)라고 알려주는 것이다. 사실 파이썬이었으면 레퍼런스 오류? 이런것으로 오류가 나는 부분이라 되게 생소했는데, 사정을 알고보니 별거 아니었다.

// checkPass()은 될까? 된다. 그리고 불합격이 출력되고 마찬가지로 디폴트 리턴까지 넘어가서 undefined가 나온다. 

// 만약 위에 console.log를 return으로 바꿨을때, 밑에 checkPass(70)이 checkPass()로 바뀌면, 자연스럽게 불합격이 출력되고 undefined같은건 없다. 왜냐하면 리턴에서 깔끔하게 끝이 났기 때문이다.

// 우리가 인자를 넣고 안넣고는 문제되지않는다.

// 다만 리턴을 썼을때 리턴 뒤에 값은 넣어줘야 한다. 


// ============================================
// 📌 코드 흐름 요약
// ============================================
// 1. for문: 반복 실행 (i++ = 1씩 증가)
// 2. for...of: 배열 요소 하나씩 꺼내서 반복
// 3. 객체: {key: value} 형태로 데이터 묶음 관리
// 4. 함수: function 이름(매개변수) { 실행코드 }
// 5. return:
//    - return 있으면 → 값 반환 후 함수 종료
//    - return 없으면 → undefined 반환 (디폴트)