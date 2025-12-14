# Coding Questions

## 25. Check if a number is a palindrome without converting to string

```java
public class PalindromeNumber {
    
    public static boolean isPalindrome(int num) {
        // Negative numbers are not palindromes
        if (num < 0) return false;
        
        // Single digit is always palindrome
        if (num < 10) return true;
        
        // Numbers ending with 0 can't be palindrome (except 0)
        if (num % 10 == 0) return false;
        
        int reversed = 0;
        int original = num;
        
        while (num > 0) {
            int digit = num % 10;
            reversed = reversed * 10 + digit;
            num /= 10;
        }
        
        return original == reversed;
    }
    
    // Optimized: Only reverse half
    public static boolean isPalindromeOptimized(int num) {
        if (num < 0 || (num % 10 == 0 && num != 0)) return false;
        
        int reversedHalf = 0;
        while (num > reversedHalf) {
            reversedHalf = reversedHalf * 10 + num % 10;
            num /= 10;
        }
        
        // For odd digits: reversedHalf/10 removes middle digit
        return num == reversedHalf || num == reversedHalf / 10;
    }
    
    public static void main(String[] args) {
        System.out.println(isPalindrome(12321));  // true
        System.out.println(isPalindrome(12345));  // false
        System.out.println(isPalindrome(1221));   // true
        System.out.println(isPalindrome(-121));   // false
    }
}
```

**Time Complexity:** O(log₁₀(n)) - number of digits  
**Space Complexity:** O(1)

---

## 26. Sort a stack using another stack

```java
import java.util.Stack;

public class SortStack {
    
    public static Stack<Integer> sort(Stack<Integer> input) {
        Stack<Integer> sorted = new Stack<>();
        
        while (!input.isEmpty()) {
            // Pop element from input
            int temp = input.pop();
            
            // Move elements from sorted to input while they're greater than temp
            while (!sorted.isEmpty() && sorted.peek() > temp) {
                input.push(sorted.pop());
            }
            
            // Push temp in correct position
            sorted.push(temp);
        }
        
        return sorted; // Sorted in ascending order (smallest at bottom)
    }
    
    // Sort in descending order (largest at top)
    public static Stack<Integer> sortDescending(Stack<Integer> input) {
        Stack<Integer> sorted = new Stack<>();
        
        while (!input.isEmpty()) {
            int temp = input.pop();
            
            while (!sorted.isEmpty() && sorted.peek() < temp) {
                input.push(sorted.pop());
            }
            
            sorted.push(temp);
        }
        
        return sorted;
    }
    
    public static void main(String[] args) {
        Stack<Integer> stack = new Stack<>();
        stack.push(34);
        stack.push(3);
        stack.push(31);
        stack.push(98);
        stack.push(92);
        stack.push(23);
        
        System.out.println("Original: " + stack);  // [34, 3, 31, 98, 92, 23]
        
        Stack<Integer> sorted = sort(stack);
        System.out.println("Sorted:   " + sorted); // [3, 23, 31, 34, 92, 98]
    }
}
```

**Time Complexity:** O(n²) - worst case each element compared with all others  
**Space Complexity:** O(n) - auxiliary stack

---

## 27. Maximum Sum Subarray (Kadane's Algorithm)

```java
public class MaxSubarraySum {
    
    /**
     * Kadane's Algorithm - finds maximum sum of contiguous subarray
     * 
     * Key insight: At each position, decide whether to:
     * 1. Extend the previous subarray (currentSum + nums[i])
     * 2. Start a new subarray from current element (nums[i])
     */
    public static int maxSubArray(int[] nums) {
        if (nums == null || nums.length == 0) {
            throw new IllegalArgumentException("Array cannot be empty");
        }
        
        int maxSum = nums[0];
        int currentSum = nums[0];
        
        for (int i = 1; i < nums.length; i++) {
            // Either extend previous subarray or start new
            currentSum = Math.max(nums[i], currentSum + nums[i]);
            maxSum = Math.max(maxSum, currentSum);
        }
        
        return maxSum;
    }
    
    /**
     * Extended version: also returns the subarray indices
     */
    public static int[] maxSubArrayWithIndices(int[] nums) {
        int maxSum = nums[0];
        int currentSum = nums[0];
        int start = 0, end = 0, tempStart = 0;
        
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] > currentSum + nums[i]) {
                currentSum = nums[i];
                tempStart = i;
            } else {
                currentSum += nums[i];
            }
            
            if (currentSum > maxSum) {
                maxSum = currentSum;
                start = tempStart;
                end = i;
            }
        }
        
        return new int[]{maxSum, start, end};
    }
    
    public static void main(String[] args) {
        int[] nums = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        
        System.out.println("Max sum: " + maxSubArray(nums)); // 6
        
        int[] result = maxSubArrayWithIndices(nums);
        System.out.printf("Max sum: %d, subarray indices: [%d, %d]%n", 
            result[0], result[1], result[2]); // Max sum: 6, indices: [3, 6]
        
        // Subarray is [4, -1, 2, 1]
        System.out.print("Subarray: ");
        for (int i = result[1]; i <= result[2]; i++) {
            System.out.print(nums[i] + " ");
        }
        // Output: 4 -1 2 1
        
        // Edge cases
        System.out.println("\n\nAll negative: " + maxSubArray(new int[]{-3, -1, -4})); // -1
        System.out.println("Single element: " + maxSubArray(new int[]{5})); // 5
        System.out.println("All positive: " + maxSubArray(new int[]{1, 2, 3})); // 6
    }
}
```

**Time Complexity:** O(n) - single pass  
**Space Complexity:** O(1) - constant extra space

**How Kadane's works step-by-step:**
```
Array: [-2, 1, -3, 4, -1, 2, 1, -5, 4]

i=0: currentSum = -2, maxSum = -2
i=1: currentSum = max(1, -2+1) = 1, maxSum = 1
i=2: currentSum = max(-3, 1-3) = -2, maxSum = 1
i=3: currentSum = max(4, -2+4) = 4, maxSum = 4
i=4: currentSum = max(-1, 4-1) = 3, maxSum = 4
i=5: currentSum = max(2, 3+2) = 5, maxSum = 5
i=6: currentSum = max(1, 5+1) = 6, maxSum = 6
i=7: currentSum = max(-5, 6-5) = 1, maxSum = 6
i=8: currentSum = max(4, 1+4) = 5, maxSum = 6

Result: 6 (subarray [4, -1, 2, 1])
```
