class Solution {
public:
    /**
     * @param root: a TreeNode, the root of the binary tree
     * @return: nothing
     */
    void flatten(TreeNode *root) {
        // write your code here
        if (root == NULL) return;  
        while (root) {  
            if (root->left) {  
                TreeNode *pre = root->left;  
                while (pre->right)  
                    pre = pre->right;  
                pre->right = root->right;  
                root->right = root->left;  
                root->left = NULL;  
            }
            root = root->right;
        }  
    }
};
