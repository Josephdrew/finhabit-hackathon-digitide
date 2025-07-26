import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:http/http.dart' as http;

class PhoneAuthPage extends StatefulWidget {
  @override
  _PhoneAuthPageState createState() => _PhoneAuthPageState();
}

class _PhoneAuthPageState extends State<PhoneAuthPage> {
  final TextEditingController phoneController = TextEditingController();
  final TextEditingController otpController = TextEditingController();
  String? verificationId;
  String? idToken;
  String backendResponse = "";

  Future<void> sendOtp() async {
    await FirebaseAuth.instance.verifyPhoneNumber(
      phoneNumber: phoneController.text,
      verificationCompleted: (PhoneAuthCredential credential) async {
        // Auto-retrieval or instant verification
        await FirebaseAuth.instance.signInWithCredential(credential);
      },
      verificationFailed: (FirebaseAuthException e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Verification failed:  ${e.message}')),
        );
      },
      codeSent: (String verId, int? resendToken) {
        setState(() {
          verificationId = verId;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('OTP sent!')),
        );
      },
      codeAutoRetrievalTimeout: (String verId) {
        setState(() {
          verificationId = verId;
        });
      },
    );
  }

  Future<void> verifyOtpAndGetIdToken() async {
    if (verificationId == null) return;
    final credential = PhoneAuthProvider.credential(
      verificationId: verificationId!,
      smsCode: otpController.text,
    );
    final userCredential = await FirebaseAuth.instance.signInWithCredential(credential);
    final user = userCredential.user;
    if (user != null) {
      final token = await user.getIdToken();
      setState(() {
        idToken = token;
      });
      // Optionally, send to backend
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/firebase/login'),
        headers: {'Content-Type': 'application/json'},
        body: '{"firebase_id_token": "$idToken"}',
      );
      setState(() {
        backendResponse = response.body;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Phone Auth & Firebase ID Token')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: phoneController,
              decoration: InputDecoration(labelText: 'Phone (+91xxxxxxxxxx)'),
            ),
            ElevatedButton(
              onPressed: sendOtp,
              child: Text('Send OTP'),
            ),
            TextField(
              controller: otpController,
              decoration: InputDecoration(labelText: 'Enter OTP'),
            ),
            ElevatedButton(
              onPressed: verifyOtpAndGetIdToken,
              child: Text('Verify OTP & Get ID Token'),
            ),
            if (idToken != null) ...[
              Text('Firebase ID Token:', style: TextStyle(fontWeight: FontWeight.bold)),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: SelectableText(idToken ?? '', style: TextStyle(fontSize: 10)),
              ),
            ],
            if (backendResponse.isNotEmpty) ...[
              SizedBox(height: 16),
              Text('Backend Response:', style: TextStyle(fontWeight: FontWeight.bold)),
              Text(backendResponse),
            ]
          ],
        ),
      ),
    );
  }
} 