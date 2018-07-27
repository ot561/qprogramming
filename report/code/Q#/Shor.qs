﻿namespace Quantum.Shor{

    open Microsoft.Quantum.Primitive;
    open Microsoft.Quantum.Canon;
	open Microsoft.Quantum.Extensions.Math;
	open Microsoft.Quantum.Extensions.Convert;


	/// # Summary
	/// Sets the given qubit to the |0> state in the computational basis
	/// # Input 
    /// ## q1
    /// The qubit to be operated on
    operation SetZero (q1: Qubit) : (){

        body{

            let current = M(q1);

            if (current != Zero){
                X(q1);
            }
        }
    }
	
	/// # Summary
	/// Given N and coprime a, calculates the approximate period of f(x) = (a^x) mod N
	/// # Input 
    /// ## N
    /// An integer, the modulus in f(x)
    /// ## a
    /// A random integer coprime to N, the base of the exponential in f(x)
    /// # Output 
    /// Int: the approximate period
	operation ApproximatePeriodicity(N: Int, a: Int) : (Int){

        body{
			let len1 = Ceiling(Log(ToDouble(N^2))/Log(ToDouble(2))); // length register 1
			let len2 = Ceiling(Log( ToDouble(N) )/Log(ToDouble(2))); // length register 2

			mutable outcome1 = 0;

			// Allocate all qubits required 
			using (qubits = Qubit[len1+len2]){

				// Create the two registers
				mutable indexReg1 = new Int[len1];
				for (i in 0..len1-1){
					set indexReg1[i] = i;
				}
				let reg1 = Subarray(indexReg1, qubits);

				mutable indexReg2 = new Int[len2];
				for (i in 0..len2-1){
					set indexReg2[i] = len1+i;
				}
				let reg2 = Subarray(indexReg2, qubits);

				// Apply H to first register
				ApplyToEach (H, reg1);

				// Apply O_f for f(x) = a^x mod N-> use method from paper of Stephane Beauregard
				for (i in 0..len1-1){
					(Controlled ModularQubitMultiplyByExp)
					            ([reg1[i]], (LittleEndian(reg2), a^2, i, N));
				}

				// Measure 2nd register
				let outcome2 = MeasureInteger(LittleEndian(reg2));

				// Apply Q_N to first register
				(Adjoint QFTLE)(LittleEndian(reg2));

				// Measure first register -> outcome k
				set outcome1 = MeasureInteger(LittleEndian(reg1));

				// Clean qubits
				ApplyToEach(SetZero, qubits);

			}
			
			return outcome1;
		}
	}
	
	/// # Summary
	/// Gives mapping |x> -> |(x*a^b) mod N)
	/// # Input 
    /// ## stateIn
    /// A Qubit[] in little endian format: |x>
    /// ## expBase
    /// The base of the exponential: a
    /// ## power
	/// The power used in the exponential: b
	/// ## modulus
	/// The value in which modulus everything is calculated: N
	/// N and a should be coprime
    /// # Output 
    /// ()
	operation ModularQubitMultiplyByExp
				(stateIn: LittleEndian, expBase: Int, power: Int, modulus: Int):(){
		
		body{
			ModularMultiplyByConstantLE(ExpMod(expBase, power, modulus), modulus, stateIn);
		}
	
		adjoint auto
		controlled auto
		controlled adjoint auto
	}
}