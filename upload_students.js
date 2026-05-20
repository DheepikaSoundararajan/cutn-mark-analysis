const admin = require('firebase-admin');

const serviceAccount = require(
  './firebase-key.json'
);

const studentsData = require(
  './students.json'
);

// ======================================
// INITIALIZE FIREBASE
// ======================================

admin.initializeApp({

  credential: admin.credential.cert(
    serviceAccount
  )

});

const db = admin.firestore();

// ======================================
// UPLOAD STUDENTS
// ======================================

async function uploadStudents() {

  const collectionRef = db.collection(
    'student'
  );

  console.log(
    '🚀 Uploading students...'
  );

  for (const student of studentsData) {

    const docId =
      student.register_number;

    try {

      await collectionRef
        .doc(docId)
        .set(student);

      console.log(

        `✅ Uploaded:
        ${student.name}
        (${docId})`

      );

    }

    catch (error) {

      console.error(

        `❌ Failed:
        ${docId}`,

        error

      );

    }

  }

  console.log(
    '🎉 All students uploaded!'
  );

}

uploadStudents();